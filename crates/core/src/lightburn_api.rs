//! Zero-dependency local HTTP client for LightBurn 2.2+'s REST API (`127.0.0.1:19520`).
//!
//! By default this module refuses non-loopback hosts so cutting geometry never
//! leaves the local machine unless the caller explicitly enables LAN mode.
//! Uses only `std::net::TcpStream` (`#![forbid(unsafe_code)]`, no extra crates).
use std::io::{Read, Write};
use std::net::{IpAddr, TcpStream, ToSocketAddrs};
use std::time::Duration;

use anyhow::{Context, Result, bail, ensure};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

pub const DEFAULT_HOST: &str = "127.0.0.1";
pub const DEFAULT_PORT: u16 = 19520;

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum SendMode {
    /// `POST /api/file/upload`: merge the sheet into LightBurn's currently open project.
    #[default]
    Upload,
    /// `POST /api/file/open`: replace LightBurn's open project with this sheet.
    Open,
}

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
pub struct ClientOptions {
    pub host: String,
    pub port: u16,
    /// Permit non-loopback LAN hosts (false by default; never upload over the internet).
    pub allow_lan: bool,
    pub timeout_seconds: u64,
}

impl Default for ClientOptions {
    fn default() -> Self {
        Self {
            host: DEFAULT_HOST.to_owned(),
            port: DEFAULT_PORT,
            allow_lan: false,
            timeout_seconds: 10,
        }
    }
}

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
pub struct ApiResponse {
    pub status_code: u16,
    pub endpoint: String,
    pub body: String,
}

fn is_loopback_host(host: &str) -> bool {
    if host.eq_ignore_ascii_case("localhost") {
        return true;
    }
    host.parse::<IpAddr>().is_ok_and(|ip| ip.is_loopback())
}

fn connect(options: &ClientOptions) -> Result<TcpStream> {
    ensure!(!options.host.trim().is_empty(), "host cannot be empty");
    ensure!(options.port > 0, "port must be positive");
    ensure!(
        options.allow_lan || is_loopback_host(&options.host),
        "refusing to send cutting files to non-loopback host {:?}; pass --allow-lan only for a trusted local LightBurn machine",
        options.host
    );
    let addr = format!("{}:{}", options.host, options.port)
        .to_socket_addrs()
        .with_context(|| format!("cannot resolve {}:{}", options.host, options.port))?
        .next()
        .with_context(|| format!("no address for {}:{}", options.host, options.port))?;
    if !options.allow_lan {
        ensure!(
            addr.ip().is_loopback(),
            "resolved address {} is not loopback",
            addr.ip()
        );
    }
    let timeout = Duration::from_secs(options.timeout_seconds.max(1));
    let stream = TcpStream::connect_timeout(&addr, timeout).with_context(|| {
        format!(
            "cannot reach LightBurn REST API at {}:{}; verify LightBurn 2.2+ is running and its local REST API is enabled",
            options.host, options.port
        )
    })?;
    stream.set_read_timeout(Some(timeout))?;
    stream.set_write_timeout(Some(timeout))?;
    Ok(stream)
}

fn read_response(stream: &mut TcpStream, endpoint: &str) -> Result<ApiResponse> {
    let mut raw = Vec::new();
    let mut buf = [0_u8; 4096];
    let mut header_end: Option<usize> = None;
    let mut content_length: Option<usize> = None;
    loop {
        match stream.read(&mut buf) {
            Ok(0) => break,
            Ok(n) => {
                raw.extend_from_slice(&buf[..n]);
                if header_end.is_none()
                    && let Some(pos) = find_header_end(&raw)
                {
                    header_end = Some(pos);
                    let head = String::from_utf8_lossy(&raw[..pos]);
                    content_length = head.lines().find_map(|line| {
                        let (k, v) = line.split_once(':')?;
                        k.trim()
                            .eq_ignore_ascii_case("content-length")
                            .then(|| v.trim().parse::<usize>().ok())
                            .flatten()
                    });
                }
                if let (Some(end), Some(len)) = (header_end, content_length)
                    && raw.len() >= end + len
                {
                    break;
                }
            }
            Err(err) if !raw.is_empty() && header_end.is_some() => {
                // Some local HTTP servers reset the socket immediately after sending
                // a complete response body; accept it if we already have all bytes.
                if content_length.is_none_or(|len| raw.len() >= header_end.unwrap() + len) {
                    break;
                }
                return Err(err).context("failed reading LightBurn REST API response");
            }
            Err(err) => return Err(err).context("failed reading LightBurn REST API response"),
        }
    }
    let text = String::from_utf8_lossy(&raw).into_owned();
    let (head, body) = text
        .split_once("\r\n\r\n")
        .or_else(|| text.split_once("\n\n"))
        .context("malformed HTTP response from LightBurn REST API")?;
    let status_line = head.lines().next().context("empty HTTP response")?;
    let status_code = status_line
        .split_whitespace()
        .nth(1)
        .and_then(|s| s.parse::<u16>().ok())
        .with_context(|| format!("unexpected HTTP status line: {status_line:?}"))?;
    if status_code == 401 || status_code == 403 {
        bail!(
            "LightBurn REST API returned HTTP {status_code} on {endpoint}: approve the pairing consent dialog inside LightBurn and retry"
        );
    }
    if !(200..300).contains(&status_code) {
        bail!(
            "LightBurn REST API returned HTTP {status_code} on {endpoint}: {}",
            body.trim()
        );
    }
    Ok(ApiResponse {
        status_code,
        endpoint: endpoint.to_owned(),
        body: body.to_owned(),
    })
}

fn find_header_end(raw: &[u8]) -> Option<usize> {
    if let Some(i) = raw.windows(4).position(|w| w == b"\r\n\r\n") {
        return Some(i + 4);
    }
    raw.windows(2).position(|w| w == b"\n\n").map(|i| i + 2)
}

/// Check that a local LightBurn REST API server is reachable (`GET /api/status`).
pub fn status(options: &ClientOptions) -> Result<ApiResponse> {
    let mut stream = connect(options)?;
    let req = format!(
        "GET /api/status HTTP/1.1\r\nHost: {}:{}\r\nUser-Agent: Nestbolt\r\nConnection: close\r\n\r\n",
        options.host, options.port
    );
    stream.write_all(req.as_bytes())?;
    stream.flush()?;
    read_response(&mut stream, "/api/status")
}

/// Send an exported `.lbrn2`, `.svg`, or `.dxf` document to a running local
/// LightBurn instance via `POST /api/file/upload` or `POST /api/file/open`.
pub fn send_file(
    options: &ClientOptions,
    mode: SendMode,
    filename: &str,
    contents: &[u8],
) -> Result<ApiResponse> {
    ensure!(!filename.trim().is_empty(), "filename cannot be empty");
    ensure!(
        !filename.contains(['\r', '\n', '"', '/', '\\']),
        "filename must be a plain file name"
    );
    ensure!(!contents.is_empty(), "file contents cannot be empty");
    let lower = filename.to_ascii_lowercase();
    let content_type = if lower.ends_with(".lbrn2") || lower.ends_with(".lbrn") {
        "application/xml"
    } else if lower.ends_with(".svg") {
        "image/svg+xml"
    } else if lower.ends_with(".dxf") {
        "application/dxf"
    } else {
        bail!("unsupported LightBurn file type {filename:?}; expected .lbrn2, .svg or .dxf");
    };
    let endpoint = match mode {
        SendMode::Upload => "/api/file/upload",
        SendMode::Open => "/api/file/open",
    };
    let boundary = "----NestboltLightBurnBoundary7f3a9c";
    let mut body = Vec::with_capacity(contents.len() + 256);
    write!(
        body,
        "--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\nContent-Type: {content_type}\r\n\r\n"
    )?;
    body.extend_from_slice(contents);
    write!(body, "\r\n--{boundary}--\r\n")?;

    let mut stream = connect(options)?;
    let mut request = format!(
        "POST {endpoint} HTTP/1.1\r\nHost: {}:{}\r\nUser-Agent: Nestbolt\r\nContent-Type: multipart/form-data; boundary={boundary}\r\nContent-Length: {}\r\nConnection: close\r\n\r\n",
        options.host,
        options.port,
        body.len()
    )
    .into_bytes();
    request.extend_from_slice(&body);
    stream.write_all(&request)?;
    stream.flush()?;
    read_response(&mut stream, endpoint)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::net::{Shutdown, TcpListener};
    use std::thread;

    fn mock_server(response: &'static str) -> (u16, thread::JoinHandle<String>) {
        let listener = TcpListener::bind("127.0.0.1:0").unwrap();
        let port = listener.local_addr().unwrap().port();
        let handle = thread::spawn(move || {
            let (mut stream, _) = listener.accept().unwrap();
            stream
                .set_read_timeout(Some(Duration::from_secs(2)))
                .unwrap();
            let mut raw = Vec::new();
            let mut buf = [0_u8; 4096];
            let mut expected = None;
            loop {
                match stream.read(&mut buf) {
                    Ok(0) => break,
                    Ok(n) => {
                        raw.extend_from_slice(&buf[..n]);
                        if expected.is_none()
                            && let Some(end) = find_header_end(&raw)
                        {
                            let head = String::from_utf8_lossy(&raw[..end]);
                            let cl = head
                                .lines()
                                .find_map(|line| {
                                    let (k, v) = line.split_once(':')?;
                                    k.trim()
                                        .eq_ignore_ascii_case("content-length")
                                        .then(|| v.trim().parse::<usize>().ok())
                                        .flatten()
                                })
                                .unwrap_or(0);
                            expected = Some(end + cl);
                        }
                        if expected.is_some_and(|need| raw.len() >= need) {
                            break;
                        }
                    }
                    Err(_) => break,
                }
            }
            stream.write_all(response.as_bytes()).unwrap();
            let _ = stream.flush();
            let _ = stream.shutdown(Shutdown::Both);
            String::from_utf8_lossy(&raw).into_owned()
        });
        (port, handle)
    }

    #[test]
    fn status_and_file_upload_work_against_local_mock_lightburn() {
        let (port, handle) =
            mock_server("HTTP/1.1 200 OK\r\nContent-Length: 15\r\n\r\n{\"ready\": true}");
        let opts = ClientOptions {
            port,
            ..ClientOptions::default()
        };
        let res = status(&opts).unwrap();
        assert_eq!(res.status_code, 200);
        assert!(res.body.contains("ready"));
        assert!(
            handle
                .join()
                .unwrap()
                .starts_with("GET /api/status HTTP/1.1")
        );

        let (port, handle) = mock_server("HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nok");
        let opts = ClientOptions {
            port,
            ..ClientOptions::default()
        };
        let res = send_file(
            &opts,
            SendMode::Upload,
            "sheet-0.lbrn2",
            b"<LightBurnProject/>",
        )
        .unwrap();
        assert_eq!(res.status_code, 200);
        let received = handle.join().unwrap();
        assert!(received.starts_with("POST /api/file/upload HTTP/1.1"));
        assert!(received.contains("filename=\"sheet-0.lbrn2\""));
        assert!(received.contains("<LightBurnProject/>"));
    }

    #[test]
    fn refuses_non_loopback_by_default_and_explains_pairing_403() {
        let remote = ClientOptions {
            host: "192.0.2.10".into(),
            ..ClientOptions::default()
        };
        let err = status(&remote).unwrap_err().to_string();
        assert!(err.contains("non-loopback"), "{err}");

        let (port, handle) =
            mock_server("HTTP/1.1 403 Forbidden\r\nContent-Length: 6\r\n\r\npaired");
        let opts = ClientOptions {
            port,
            ..ClientOptions::default()
        };
        let err = send_file(&opts, SendMode::Open, "sheet-0.svg", b"<svg/>")
            .unwrap_err()
            .to_string();
        assert!(err.contains("pairing consent dialog"), "{err}");
        let _ = handle.join();
    }
}
