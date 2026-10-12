//! Cooperative interruption shared by native and browser search. A collision
//! quota is deterministic; an external cancellation/deadline is not a work quota.
use std::{error::Error, fmt};

use serde::Serialize;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum StopReason {
    WorkLimit,
    Cancelled,
    Deadline,
}

#[derive(Debug)]
pub struct Interrupted(pub StopReason);

impl fmt::Display for Interrupted {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "search interrupted: {:?}", self.0)
    }
}
impl Error for Interrupted {}

pub struct Control<'a> {
    limit: Option<u64>,
    used: u64,
    probe: Option<&'a mut dyn FnMut() -> Option<StopReason>>,
    stopped: Option<StopReason>,
}

impl<'a> Control<'a> {
    pub fn new(
        limit: Option<u64>,
        probe: Option<&'a mut dyn FnMut() -> Option<StopReason>>,
    ) -> Self {
        Self {
            limit,
            used: 0,
            probe,
            stopped: None,
        }
    }

    pub fn unlimited() -> Self {
        Self::new(None, None)
    }

    pub fn collision_checks(&self) -> u64 {
        self.used
    }

    pub fn stop_reason(&self) -> Option<StopReason> {
        self.stopped
    }

    /// Check between geometry imports, parts and passes. Individual upstream
    /// geometry calls and independent validation are not preempted midway.
    pub(crate) fn checkpoint(&mut self) -> Result<(), Interrupted> {
        if self.stopped.is_none() {
            self.stopped = self.probe.as_mut().and_then(|probe| probe());
        }
        self.stopped
            .map_or(Ok(()), |reason| Err(Interrupted(reason)))
    }

    pub(crate) fn before_collision(&mut self) -> Result<(), Interrupted> {
        if self.used.is_multiple_of(64) || self.stopped.is_some() {
            self.checkpoint()?;
        }
        if self.limit.is_some_and(|limit| self.used >= limit) {
            self.stopped = Some(StopReason::WorkLimit);
            return Err(Interrupted(StopReason::WorkLimit));
        }
        self.used += 1;
        Ok(())
    }
}
