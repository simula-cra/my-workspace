<#
.SYNOPSIS
    Claude Codeが書いた作業指示書を、Antigravity CLI（agy）にヘッドレスで実行させる。

.DESCRIPTION
    役割分担:
      Claude Code … 設計・指示書作成・結果レビュー・git commit（考える側）
      Antigravity … 指示書どおりの実作業（手を動かす側。無料枠を使う）

    このスクリプトは「渡して、待って、結果を保存する」だけ。判断はしない。
    実行のたびに runs\<日時>\ に指示書・生出力・応答・メタ情報を残すので、
    Claude Codeは後からそこを読んでレビューできる。

    重要: agy にgitのcommit/pushはさせない（指示書テンプレートの「やらないこと」に明記）。
    差分のレビューとcommitはClaude Code側の仕事。

.PARAMETER SpecPath
    作業指示書（Markdown）。WorkDir の中に置くこと。

.PARAMETER WorkDir
    agy を動かすフォルダ。既定はカレント。

.PARAMETER AutoApprove
    agy の --dangerously-skip-permissions を付ける。無人実行向け。
    既定はオフ（承認が取れないツールはソフト拒否され、処理は続行される）。

.EXAMPLE
    .\Invoke-Antigravity.ps1 -SpecPath .\specs\20260918-inbox-整理.md -WorkDir C:\Users\cloch\my-workspace

.EXAMPLE
    .\Invoke-Antigravity.ps1 -SpecPath .\specs\調査-xxx.md -Effort high -TimeoutMinutes 30 -AutoApprove

.NOTES
    終了コード: 0=成功 / 1=agyがERROR等 / 2=前提不足（agy未導入・指示書なし）/ 3=無料枠切れの疑い
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SpecPath,

    [string]$WorkDir = (Get-Location).Path,

    [string]$Model,

    [ValidateSet('low', 'medium', 'high')]
    [string]$Effort = 'medium',

    [int]$TimeoutMinutes = 20,

    [string]$ConversationId,

    [switch]$AutoApprove,

    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

# --- agy を探す ---------------------------------------------------------
$agy = $null
$cmd = Get-Command 'agy' -ErrorAction SilentlyContinue
if ($cmd) {
    $agy = $cmd.Source
} elseif ($env:LOCALAPPDATA) {
    $fallback = Join-Path $env:LOCALAPPDATA 'agy\bin\agy.exe'
    if (Test-Path -LiteralPath $fallback) { $agy = $fallback }
}
if (-not $agy) {
    Write-Warning @"
agy（Antigravity CLI）が見つかりません。
PowerShellで次を実行してインストールし、一度 agy を対話起動してGoogleログインを済ませてください:
  irm https://antigravity.google/cli/install.ps1 | iex
ヘッドレス実行はキャッシュ済みの認証情報を使うため、先に対話ログインが必要です。
"@
    exit 2
}

# --- 指示書 -------------------------------------------------------------
if (-not (Test-Path -LiteralPath $SpecPath)) {
    Write-Warning "作業指示書が見つかりません: $SpecPath"
    exit 2
}
$specFull = (Resolve-Path -LiteralPath $SpecPath).Path
$workFull = (Resolve-Path -LiteralPath $WorkDir).Path

if (-not $specFull.StartsWith($workFull, [StringComparison]::OrdinalIgnoreCase)) {
    Write-Warning "指示書が作業フォルダの外にあります。agyが読めない可能性があります。`n  指示書: $specFull`n  作業先: $workFull"
}

# --- 実行の準備 ---------------------------------------------------------
$stamp  = Get-Date -Format 'yyyyMMdd-HHmmss'
$runDir = Join-Path $PSScriptRoot "runs\$stamp"
if (-not $DryRun) { New-Item -ItemType Directory -Path $runDir -Force | Out-Null }

# プロンプトは1行に保つ（改行入りの長い引数はPowerShell 5.1で壊れやすい）。
# 中身は指示書ファイルをagyに読ませる。
$prompt = "作業指示書 '$specFull' を読み、その内容に従って作業してください。指示書の「やらないこと」は厳守してください。完了したら、変更したファイルと判断した理由を簡潔に報告してください。"

$agyArgs = @(
    '-p', $prompt,
    '--output-format', 'json',
    '--effort', $Effort,
    '--print-timeout', "$($TimeoutMinutes)m"
)
if ($Model)          { $agyArgs += @('--model', $Model) }
if ($ConversationId) { $agyArgs += @('--conversation', $ConversationId) }
if ($AutoApprove)    { $agyArgs += '--dangerously-skip-permissions' }

Write-Host "指示書 : $specFull"
Write-Host "作業先 : $workFull"
Write-Host "agy    : $agy"
Write-Host "引数   : $($agyArgs -join ' ')"
Write-Host ""

if ($DryRun) {
    Write-Host "DryRun のため実行しません。"
    exit 0
}

Copy-Item -LiteralPath $specFull -Destination (Join-Path $runDir 'spec.md') -Force

# --- 実行 ---------------------------------------------------------------
$outFile = Join-Path $runDir 'stdout.json'
$errFile = Join-Path $runDir 'stderr.txt'
$started = Get-Date

Push-Location $workFull
try {
    $proc = Start-Process -FilePath $agy -ArgumentList $agyArgs `
        -NoNewWindow -Wait -PassThru `
        -RedirectStandardOutput $outFile -RedirectStandardError $errFile
    $exitCode = $proc.ExitCode
} finally {
    Pop-Location
}
$elapsed = (Get-Date) - $started

# --- 結果の解釈 ---------------------------------------------------------
# agy は部分出力のタイムアウト時でも exit 0 を返すことがあるため、
# 終了コードではなく JSON の status を正とする。
$raw     = if (Test-Path -LiteralPath $outFile) { Get-Content -LiteralPath $outFile -Raw } else { '' }
$stderr  = if (Test-Path -LiteralPath $errFile) { Get-Content -LiteralPath $errFile -Raw } else { '' }
$status  = 'UNKNOWN'
$response = ''
$convId  = ''
$errMsg  = ''

if ($raw) {
    try {
        $json = $raw | ConvertFrom-Json
        if ($json.PSObject.Properties.Name -contains 'status')          { $status   = $json.status }
        if ($json.PSObject.Properties.Name -contains 'response')        { $response = $json.response }
        if ($json.PSObject.Properties.Name -contains 'conversation_id') { $convId   = $json.conversation_id }
        if ($json.PSObject.Properties.Name -contains 'error')           { $errMsg   = $json.error }
    } catch {
        Write-Warning "agyの出力をJSONとして解釈できませんでした。stdout.json を直接確認してください。"
    }
}

if ($response) { Set-Content -LiteralPath (Join-Path $runDir 'response.md') -Value $response -Encoding UTF8 }

[pscustomobject]@{
    実行日時       = $started.ToString('yyyy-MM-dd HH:mm:ss')
    所要           = "{0:n1} 分" -f $elapsed.TotalMinutes
    指示書         = $specFull
    作業先         = $workFull
    status         = $status
    exitCode       = $exitCode
    conversationId = $convId
    error          = $errMsg
} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $runDir 'meta.json') -Encoding UTF8

Write-Host "status   : $status  (exit $exitCode, $("{0:n1}" -f $elapsed.TotalMinutes) 分)"
if ($convId) { Write-Host "続きから: -ConversationId $convId" }
Write-Host "記録     : $runDir"
Write-Host ""

if ($response) {
    Write-Host "--- agyの報告 ---"
    Write-Host $response
    Write-Host "-----------------"
    Write-Host ""
}

# --- 無料枠切れの判定 ---------------------------------------------------
$quotaPattern = 'quota|rate.?limit|RESOURCE_EXHAUSTED|429|usage limit|weekly limit'
if (("$errMsg`n$stderr`n$raw") -match $quotaPattern) {
    Write-Warning @"
Antigravityの無料枠を使い切った可能性があります。
無料枠は週次で補充される仕様で、公開された具体的な数値はありません。
・急ぐ作業はClaude Code側で片付ける
・急がない作業は指示書を specs\ に残しておき、枠が戻ってから再投入する
"@
    exit 3
}

if ($status -ne 'SUCCESS') {
    Write-Warning "成功しませんでした（status=$status）。stderr.txt と stdout.json を確認してください。"
    exit 1
}

Write-Host "完了。次はClaude Codeが差分をレビューしてcommitします（git diff）。"
exit 0
