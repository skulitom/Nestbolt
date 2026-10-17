# Nestbolt

[English](https://github.com/skulitom/Nestbolt/blob/main/README.md) · [简体中文](https://github.com/skulitom/Nestbolt/blob/main/README.zh-CN.md) · 日本語

> このページは英語版 README の冒頭部分を要約した翻訳です。内容に違いがある場合は[英語版 README](https://github.com/skulitom/Nestbolt/blob/main/README.md) が優先されます。

Nestbolt は、**サイズの決まった板材**から切り出す人のための、無料でオープンソース（MIT）のネスティング（板取り）ツールです。対象はレーザーカッター、CNC ルーター、プラズマ、ウォータージェット、そして布や革の裁断です。材料の使用量ができるだけ少なくなるように部品を配置します。[ブラウザで動作し](https://skulitom.github.io/Nestbolt/)（ファイルは一切アップロードされません）、コマンドラインツールとしても、AI エージェントが呼び出せる MCP サーバーとしても使えます。

[ブラウザ版を開く](https://skulitom.github.io/Nestbolt/) ·
[リリースをダウンロード](https://github.com/skulitom/Nestbolt/releases) ·
[AI エージェントを接続する](https://github.com/skulitom/Nestbolt/blob/main/docs/AGENT_INTERFACE.md)

## 比較結果

凍結された v1 ベンチマークでは、同じ 60 秒の時間予算で、ジョブごとに Deepnest・SVGnest・Sparrow のうち最も良い結果と比べ、中央値で **8.5% 少ない材料**で済み、300 秒の予算では 9.6% 少なくなりました。これは最終ベンチマーク実行（新しいシード、調整に使っていない 10 件のジョブを含む）の結果です。60 秒の予算では、56 件中 8 件で Sparrow がまだ勝っています。

| 時間予算 | Nestbolt の有効なレイアウト | 最良の競合より少ない材料（中央値） | 勝ちまたは引き分け |
| --- | ---: | ---: | ---: |
| 60 秒 | 375/375 | **8.5%** | 56 件中 48 件 |
| 300 秒（長時間サブセット） | 60/60 | **9.6%** | 11 件中 11 件 |

最終受け入れ実行（2026-10-13）：凍結された 75 件の板材ジョブ（学術 35 件、メイカー 40 件。うち 10 件はどの調整にも使っていません）、各ツールで同じ時間予算と 1 CPU コア、ジョブごとに 5 つの新しいシードを使い、すべてのレイアウトを独立した検証器でチェックしました。詳しくは[英語版 README の比較セクション](https://github.com/skulitom/Nestbolt/blob/main/README.md#how-it-compares)と[すべての結果](https://skulitom.github.io/Nestbolt/results/)をご覧ください。

## 例

![451 個の文字の輪郭を 1 枚の板に配置。小さな文字が大きな文字の穴の中に入っている](docs/images/showcase.png)

1 CPU コアで 120 秒かけて、451 個の部品を 850 × 425 mm の板 1 枚に配置しました。4 サイズの DejaVu Sans Bold のグリフを、正確なベジェ輪郭、90° 回転、1 mm 間隔で使っています。29 文字が他の文字の穴の中に収まり、未使用の材料は上部にきれいな端材 1 つとして残ります。このレイアウトは独立した検証器を通過しています。

## バージョン

- **安定版 v0.1.0** は引き続きダウンロードできます。ホストされているブラウザ版も v0.1.0 です。
- **[v0.2.0-alpha.1 プレビュー](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)**：編集可能な LightBurn プロジェクトのネスティング（**プレビュー機能**）、リードイン用の余白、大きな曲線図面の改善を含みます。Windows x64、Linux x64、macOS Apple シリコン向けのツールと、Windows 用 MCP バンドルがあります。インポートの受け入れ検証と共通線カットでの材料使用量はまだ開発中で、v1.1 計画は 60% 完了しています。上のベンチマークの数値は凍結された `75cbb32` ビルドのもので、このプレビューでは競合ツールとの新しい比較は行っていません。

## AI エージェントでの利用

MCP サーバー `nestbolt-mcp` には `import_parts`、`nest`、`validate_layout`、`export_layout`、`estimate_sheets` の 5 つのツールがあります。ネットワーク、アカウント、認証情報は不要です。すべてのパスはワークスペース内にある必要があり、ファイルを上書きすることはありません。`estimate_sheets` は下限を示すだけで、レイアウトではありません。Nestbolt は機械の安全性や適合性を保証しません。

Claude Code ではプラグインもインストールできます（先に v0.1.0 リリースのアーカイブに含まれる `nestbolt-mcp` を PATH に置いてください）：

```text
/plugin marketplace add https://raw.githubusercontent.com/skulitom/Nestbolt/main/.claude-plugin/marketplace.json
/plugin install nestbolt@nestbolt
```

詳しくは[エージェントインターフェースのドキュメント](https://github.com/skulitom/Nestbolt/blob/main/docs/AGENT_INTERFACE.md)（英語）をご覧ください。

## ライセンス

Nestbolt は [MIT](https://github.com/skulitom/Nestbolt/blob/main/LICENSE) ライセンスです。jagua-rs は改変していない MPL-2.0 の依存関係で、`crates/core/src/separate.rs` のセパレーターは Sparrow（MIT）から派生したものです。
