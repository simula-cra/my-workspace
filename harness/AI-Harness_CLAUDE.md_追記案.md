# `AI-Harness\CLAUDE.md` への追記案

運用カードの未解決「AI-HarnessのCLAUDE.mdの『パス依存』に、スタートアップの分を追記する」用。
PC側で `git status` を確認してから、`CLAUDE.md` の「パス依存」節に以下を貼る。

---

## パス依存（フォルダを動かす・名前を変えると壊れる箇所）

`AI-Harness` および `hermes` のパスは、以下に直接書き込まれている。
移動・改名するときは、**5か所すべてを同時に直す**こと。1か所でも漏れると、
自動取込はエラーを出さずに黙って止まる。

1. タスクスケジューラ `HermesPipeline_DriveSync` の設定（実行コマンド・作業フォルダ）
2. `hermes/startup_sync.vbs`（2行）
3. `hermes/Gemini_取込整理.vbs`
4. `hermes/start_chat_server.vbs`
5. **スタートアップフォルダに置かれた `start_chat_server.vbs` の実行用コピー**
   （`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`）
   2026-09-10 の `Hermes-Pipeline` → `AI-Harness` 移動ではここが漏れ、
   PC起動時に「指定されたファイルが見つかりません（80070002）」が出た。
   **コピーではなくショートカットを置くか、不要なら削除する。**

点検は `my-workspace/harness/Check-Harness.ps1` で一括確認できる。

### .vbs を新規作成・編集するとき

日本語コメントを含む `.vbs` は必ず **UTF-16LE（BOM付き）** で保存する。
UTF-8（BOMなし）だとWSHがShift-JISと誤認し、`オブジェクトがありません: 'shell'`
（800A01A8）などのランタイムエラーになる（2026-08-31に発生・修正済み）。

---

**補足**: 5番を「ショートカットにする」方針で確定した場合は、上の5番の文言を
「スタートアップに置く `start_chat_server.lnk`（本体へのショートカット。コピーを置かない）」
に置き換える。削除で確定した場合は、5番を丸ごと落として4項目にし、
「スタートアップには何も置かない」と1行足す。
