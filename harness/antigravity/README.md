# Antigravity委譲キット

**Claude Codeが設計・管理し、実作業はAntigravityの無料枠に出す**ための仕組み。
自宅デスクトップPCで動かす。

## なぜ動くか（調査結果 2026-09-18）

Antigravityには **CLI（`agy`）があり、ヘッドレス実行できる**。
これが決め手で、Claude Codeからコマンド一発で仕事を渡せる。

- `agy -p "<指示>" --output-format json` で単発実行 → JSONで結果が返る
- 認証は**Googleアカウントのログインのみ**（APIキー不要＝無料枠のまま使える）
- ヘッドレスはキャッシュ済み認証を使うので、**先に一度だけ対話ログインが必要**
- `--model` / `--effort` / `--conversation`（続きから）/ `--print-timeout` あり
- `--dangerously-skip-permissions` で全ツール自動承認（無人実行向け）

出典: [Headless mode | Antigravity Docs](https://antigravity.google/docs/cli/headless/) ／
[antigravity-cli (GitHub)](https://github.com/google-antigravity/antigravity-cli) ／
[Plans | Antigravity Docs](https://antigravity.google/docs/plans/)

## セットアップ（PCで1回だけ）

1. インストール（PowerShell）

   ```
   irm https://antigravity.google/cli/install.ps1 | iex
   ```

   `agy` は `C:\Users\cloch\AppData\Local\agy\bin` に入る。

2. **対話で1回起動してGoogleログイン**（これをやらないとヘッドレスが認証エラーで落ちる）

   ```
   agy
   ```

   配色・表示モード・ワークスペースの信頼を聞かれるので答える。

3. 動作確認

   ```
   agy -p "このフォルダのファイルを一覧して" --output-format json
   ```

## 使い方

```
# 1. Claude Codeが指示書を書く（templates\ から）
#    → specs\20260918-xxx.md

# 2. 投げる
.\Invoke-Antigravity.ps1 -SpecPath .\specs\20260918-xxx.md -WorkDir C:\Users\cloch\my-workspace

# 3. 結果は runs\<日時>\ に残る
#    spec.md / stdout.json / stderr.txt / response.md / meta.json

# 4. Claude Codeが git diff をレビューして commit
```

主なオプション:

| オプション | 用途 |
| --- | --- |
| `-Effort low\|medium\|high` | 推論の深さ。既定 medium。単純作業は low で枠を節約 |
| `-TimeoutMinutes 30` | 長い作業のとき。既定20分 |
| `-AutoApprove` | 全ツール自動承認。**信頼できる指示書のときだけ** |
| `-ConversationId <id>` | 前回の続きから。前回実行時に表示される |
| `-DryRun` | 実行せずコマンドだけ確認 |

## ファイル

| ファイル | 中身 |
| --- | --- |
| `Invoke-Antigravity.ps1` | 指示書をagyに渡して結果を保存するラッパー |
| `CLAUDE.md` | **Claude Code向けの委譲ルール**（何を出す・何を出さない・レビュー手順） |
| `templates/作業指示書テンプレート.md` | 実装・修正を頼むとき |
| `templates/調査指示書テンプレート.md` | 調べ物を頼むとき |
| `specs/` | 実際の指示書（実行のたびに追加される） |
| `runs/` | 実行記録（gitには載せない） |

## 無料枠について（正直なところ）

Antigravityの無料枠は「意味のある量を週次で補充」とだけ書かれていて、
**具体的な数値は公開されていない**。2025年11月の提供開始時は250リクエスト/日だったが、
12月に大幅削減され、2026年3月にクレジット制へ変更された経緯がある。

つまり **枠は当てにできない**。この仕組みは枠切れを前提に作ってある
（終了コード3で検出し、指示書は `specs\` に残るので枠が戻ったら再投入できる）。

## 調べ物について：Perplexityは使えない

**結論：Perplexityの無料枠では、この自動化に組み込めない。**

- Sonar APIに無料枠はない（公式の料金ページに記載なし）。Sonarは $1/1M〜、
  さらに1,000リクエストあたり $5〜$14 のリクエスト料がかかる
- Proに付いていた月$5のAPIクレジットは2026年2月に廃止された
- 無料の消費者向けPerplexityは**ブラウザで手で使う分だけ**（Pro検索・Deep Researchが各5回/日程度）。
  APIがないので、Claude Codeから自動で呼べない

出典: [Pricing | Perplexity Docs](https://docs.perplexity.ai/getting-started/pricing)

### 代わりにどうするか

1. **まずはAntigravityに調べさせる（追加登録ゼロ）** ← 既定
   Antigravityにはブラウザのサブエージェントが標準で付いている。
   `templates/調査指示書テンプレート.md` を使えば、出典URL付きのMarkdownで返ってくる。
   同じ無料枠を食うのが唯一の欠点。
2. **軽い確認はClaude Code自身のWeb検索**（枠を使わない。1〜2件の事実確認向き）
3. **枠が足りなくなったら検索APIを足す。無料枠が実在するのは:**
   - **Exa** — 登録時$20＋**毎月$10が継続的に無料**、カード登録不要
   - **Tavily** — 月1,000クレジット無料、カード登録不要
   - Brave Search APIの無料プランは2026年2月に廃止（新規は$5クレジットのみ、カード必要）

   どちらもMCPサーバーがあるので、Antigravity側にMCPとして足せば
   ブラウザ操作より少ない手数で調べられる。**必要になってからで十分。**

出典: [Best Free Web Search APIs for AI Agents 2026 | Parallel](https://parallel.ai/articles/best-free-web-search-api) ／
[7 Free Web Search APIs Compared | iTechGuides](https://www.itechguides.com/7-free-web-search-apis-for-ai-agents-free-tiers-compared/)
