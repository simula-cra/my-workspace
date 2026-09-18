# CLAUDE.md — my-workspace

クラさん（小崎大樹）の作業用リポジトリ。**自宅デスクトップPCとクラウド側のClaudeセッションで
同じファイルを共有する**ための置き場。コードの本番ではなく、PCで動かす道具を置く場所。

## セッション開始時に知っておくこと

新しいセッションは毎回ここから調べ直すことになる。以下は調べ直さなくていい既知の事実。

### どこに何があるか

| 層 | 置くもの | 場所 |
| --- | --- | --- |
| 案件の確定事項・未決 | 事実の正 | Notion 案件ナレッジDB `collection://83809175-1106-4706-bdd5-86c8931173c4` |
| 自宅PC自動化の運用 | 手順の正 | Notion「🧭 自宅PC自動化 運用カード」`3d893ac16efe810ea52ad8a9eaa333dc` |
| 思想・考え方 | クラさん本人の思考 | Obsidian Vault（`obsidian-vault` リポジトリ） |
| PCで動かす道具 | スクリプト・手順書 | **ここ**（`harness/`） |

**Obsidianは検索対象にしない。** クラさん本人の思考の箱で、二重管理になる。
案件の事実はNotionを引く。記憶で答えない。

### 自宅PCの構成（2026-09-18時点）

- 本体: `C:\Users\cloch\AI-Harness\hermes`（2026-09-10に `Hermes-Pipeline` から移動）
- 自動取込: タスクスケジューラ `HermesPipeline_DriveSync`、3時間おき
- 経路: スマホGemini →（Docsにエクスポート）→ マイドライブ直下 → Obsidian Inbox → Knowledge
  → 処理済みは Drive「999：Obsidian行き」（`1kJ9dmVzI2yuEDFNZnd-hTWPjm5vzLQbf`）へ移動
- Claudeが作るDriveファイルは「001：Claude Works」（`1URMBLp4tjBQGZ6TySimMxyR8ua6hfSK7`）へ
- **取込はObsidianが起動していないと動かない。壊れてもエラーを出さずに黙って止まる**

### クラウドセッションからPCには触れない

このセッションはAnthropicのクラウドコンテナで動く。`C:\Users\cloch\...` には到達できない。
PCで動かす必要があるものは、このリポジトリにスクリプトとして置き、クラさんに実行してもらう。

## このリポジトリの約束

- ブランチ: `claude/<内容>-<id>` で作業し、mainに直接pushしない
- PowerShellスクリプトは **UTF-8 BOM付き** で保存する（Windows PowerShell 5.1が日本語を誤読するため）
- `.vbs` に日本語コメントを入れるときは **UTF-16LE BOM付き**（UTF-8だとWSHが800A01A8で落ちる）
- PCで未検証のものは「未検証」と書く。動作確認したことにしない

## フォルダ

| フォルダ | 中身 |
| --- | --- |
| [`harness/`](harness/) | AI-Harnessの点検・修理スクリプト |
| [`harness/antigravity/`](harness/antigravity/) | Antigravity委譲キット（委譲ルールは同フォルダの `CLAUDE.md`） |
| `.claude/commands/` | スラッシュコマンド |
