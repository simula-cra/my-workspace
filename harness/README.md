# AI-Harness 運用キット

自宅デスクトップPC（`C:\Users\cloch\AI-Harness`）で動いている自動化まわりを、
点検・修理するためのスクリプト置き場。**このリポジトリ自体は何も自動実行しない。**
PC側で手で走らせるためのもの。

正となる運用情報はNotionの「🧭 自宅PC自動化 運用カード」。ここはその作業の道具。

## 使い方（デスクトップPCで）

1. Git Bash か PowerShell を開く
2. このリポジトリを取得（初回のみ）

   ```
   cd %USERPROFILE%
   git clone https://github.com/simula-cra/my-workspace.git
   ```

   2回目以降は `cd %USERPROFILE%\my-workspace` して `git pull`

3. まず健康診断（**読むだけ。何も変えない**）

   ```
   powershell -ExecutionPolicy Bypass -File "%USERPROFILE%\my-workspace\harness\Check-Harness.ps1" -ReportPath "%USERPROFILE%\Desktop\harness-report.md"
   ```

   デスクトップに `harness-report.md` ができる。**これをClaudeに投げれば状況が伝わる。**

4. 起動時エラー（80070002）を片付ける

   ```
   :: 何が起きるか見るだけ
   powershell -ExecutionPolicy Bypass -File "%USERPROFILE%\my-workspace\harness\Fix-StartupChatServer.ps1" -Mode Delete -DryRun

   :: 実行
   powershell -ExecutionPolicy Bypass -File "%USERPROFILE%\my-workspace\harness\Fix-StartupChatServer.ps1" -Mode Delete
   ```

   チャットページを残したい場合は `-Mode Delete` を `-Mode Shortcut` に変える。
   削除したファイルは `AI-Harness\hermes\_backup` に日時付きで退避される。

## スクリプト

| ファイル | 何をするか | 変更するか |
| --- | --- | --- |
| `Check-Harness.ps1` | フォルダ・タスクスケジューラ・スタートアップ・.vbsの文字コード・ログ・常駐プロセスを一括点検 | しない |
| `Fix-StartupChatServer.ps1` | スタートアップに残った旧パスの `start_chat_server.vbs` を削除、またはショートカットに置き換え | する（退避あり） |
| `AI-Harness_CLAUDE.md_追記案.md` | PC側 `AI-Harness\CLAUDE.md` に足すべき文面 | しない（手で貼る） |
| [`antigravity/`](antigravity/) | Claude Codeが設計し、実作業をAntigravityの無料枠に出すための委譲キット | する（agyが作業する） |

## 前提（2026-09-17時点で把握している構成）

- 本体: `C:\Users\cloch\AI-Harness\hermes`（2026-09-10に `Hermes-Pipeline` から移動）
- 自動取込: タスクスケジューラ `HermesPipeline_DriveSync`、3時間おき
- 取込が動くにはObsidianが起動している必要がある
- 自動取込はパスが壊れても**エラーを出さずに黙って止まる**
- `.vbs` に日本語コメントを入れるときは **UTF-16LE（BOM付き）** で保存する
  （UTF-8 BOMなしだとWSHがShift-JISと誤認して 800A01A8 で落ちる）
