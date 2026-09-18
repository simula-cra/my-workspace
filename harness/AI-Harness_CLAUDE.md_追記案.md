# `AI-Harness\CLAUDE.md` への追記案

運用カードの未解決「AI-HarnessのCLAUDE.mdの『パス依存』に、スタートアップの分を追記する」用。
PC側で `git status` を確認してから、`CLAUDE.md` の「パス依存」節に以下を貼る。

---

## パス依存（フォルダを動かす・名前を変えると壊れる箇所）

`AI-Harness` および `hermes` のパスは、以下に直接書き込まれている。
移動・改名するときは、**4か所すべてを同時に直す**こと。1か所でも漏れると、
自動取込はエラーを出さずに黙って止まる。

1. タスクスケジューラ `HermesPipeline_DriveSync` の設定（実行コマンド・作業フォルダ）
2. `hermes/startup_sync.vbs`（2行）
3. `hermes/Gemini_取込整理.vbs`
4. `hermes/start_chat_server.vbs`

**スタートアップフォルダ（`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`）には
何も置かない。** 2026-09-10 の `Hermes-Pipeline` → `AI-Harness` 移動では、ここに置かれていた
`start_chat_server.vbs` の実行用コピーだけが旧パスを指したまま残り、PC起動時に
「指定されたファイルが見つかりません（80070002）」が出た。
2026-09-18に**削除で確定**（チャットページが使う `hermes3:8b` は不採用モデルで、8/26以降未使用）。
今後もしスタートアップに何か登録する必要が出たら、**コピーではなくショートカットを置く**こと。

点検は `my-workspace/harness/Check-Harness.ps1` で一括確認できる。
削除の実行は `my-workspace/harness/Fix-StartupChatServer.ps1 -Mode Delete`。

### .vbs を新規作成・編集するとき

日本語コメントを含む `.vbs` は必ず **UTF-16LE（BOM付き）** で保存する。
UTF-8（BOMなし）だとWSHがShift-JISと誤認し、`オブジェクトがありません: 'shell'`
（800A01A8）などのランタイムエラーになる（2026-08-31に発生・修正済み）。

---

**この文面は2026-09-18に確定済み。** そのまま `AI-Harness\CLAUDE.md` の「パス依存」節に貼れる。
