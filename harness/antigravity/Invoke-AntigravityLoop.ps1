<#
.SYNOPSIS
    「やらせて、検証して、ダメなら直させる」をAntigravityに回させるループ。

.DESCRIPTION
    Invoke-Antigravity.ps1 が「1回投げる」のに対し、こちらは
    目標 → 実行 → 検証 → 修正 を、合格するか上限に達するまで繰り返す。

    ループ設計（Loop Engineering）の要点をそのまま形にしてある:
      - 停止条件   … VerifyCommand が終了コード0を返したら合格。それ以外は不合格
      - 批評役     … 合否を決めるのはagyの自己申告ではなく VerifyCommand の終了コード
      - 上限       … MaxAttempts で必ず止まる。無限ループを作らない
      - 文脈の衛生 … 次の試行に渡すのは「直前の失敗」だけ。全履歴を積み上げない
      - 予算       … 無料枠切れ（終了コード3）を検知したら、試行を残して即中断する

    **VerifyCommand が本体。** ここが弱いと、通っていないものが通ったことになる。
    「テストが通る」「ビルドが通る」「特定の文字列がファイルにある」など、
    機械が判定できるものを書くこと。書けないなら、まだループに載せる段階ではない。

.PARAMETER VerifyCommand
    合否を判定するコマンド。終了コード0で合格。
    例: 'python -m pytest tests/ -q'
    例: 'node --check build_pages.js'
    例: 'if (Select-String -Path .\out.md -Pattern "## 結論" -Quiet) { exit 0 } else { exit 1 }'

.EXAMPLE
    .\Invoke-AntigravityLoop.ps1 `
        -SpecPath .\specs\20260918-テスト修正.md `
        -VerifyCommand 'python -m pytest tests/ -q' `
        -WorkDir C:\Users\cloch\my-workspace `
        -MaxAttempts 3

.NOTES
    終了コード: 0=合格 / 1=上限まで不合格 / 2=前提不足 / 3=無料枠切れで中断
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SpecPath,

    [Parameter(Mandatory = $true)]
    [string]$VerifyCommand,

    [string]$WorkDir = (Get-Location).Path,

    [ValidateRange(1, 10)]
    [int]$MaxAttempts = 3,

    [string]$Model,

    [ValidateSet('low', 'medium', 'high')]
    [string]$Effort = 'medium',

    [int]$TimeoutMinutes = 20,

    [switch]$AutoApprove,

    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$dispatcher = Join-Path $PSScriptRoot 'Invoke-Antigravity.ps1'
if (-not (Test-Path -LiteralPath $dispatcher)) {
    Write-Warning "Invoke-Antigravity.ps1 が同じフォルダに見つかりません: $dispatcher"
    exit 2
}
if (-not (Test-Path -LiteralPath $SpecPath)) {
    Write-Warning "作業指示書が見つかりません: $SpecPath"
    exit 2
}

$specFull   = (Resolve-Path -LiteralPath $SpecPath).Path
$workFull   = (Resolve-Path -LiteralPath $WorkDir).Path
$specBody   = Get-Content -LiteralPath $specFull -Raw
$stamp      = Get-Date -Format 'yyyyMMdd-HHmmss'
$loopDir    = Join-Path $PSScriptRoot "runs\loop-$stamp"
$iterSpec   = Join-Path (Split-Path -Parent $specFull) ".loop-$stamp.md"

Write-Host "=== Antigravity ループ ==="
Write-Host "指示書   : $specFull"
Write-Host "作業先   : $workFull"
Write-Host "検証     : $VerifyCommand"
Write-Host "上限     : $MaxAttempts 回"
Write-Host ""

if ($DryRun) {
    Write-Host "DryRun のため実行しません。"
    exit 0
}

New-Item -ItemType Directory -Path $loopDir -Force | Out-Null

function Invoke-Verify {
    # 批評役。標準出力・標準エラーをまとめて返し、終了コードで合否を決める。
    param([string]$Command, [string]$Directory)

    Push-Location $Directory
    try {
        $global:LASTEXITCODE = 0
        $output = & {
            try { Invoke-Expression $Command 2>&1 | Out-String }
            catch { $global:LASTEXITCODE = 1; $_ | Out-String }
        }
        $code = if ($null -eq $LASTEXITCODE) { 0 } else { $LASTEXITCODE }
    } finally {
        Pop-Location
    }
    [pscustomobject]@{ ExitCode = $code; Output = $output }
}

$log        = New-Object System.Collections.Generic.List[string]
$lastVerify = $null
$verdict    = 'FAILED'
$used       = 0

for ($attempt = 1; $attempt -le $MaxAttempts; $attempt++) {
    $used = $attempt
    Write-Host "--- 試行 $attempt / $MaxAttempts ---"

    # 次の試行に渡すのは「直前の失敗」だけ。履歴を積み上げない（文脈の衛生）。
    $body = $specBody
    if ($lastVerify) {
        $trimmed = $lastVerify.Output
        if ($trimmed.Length -gt 4000) { $trimmed = $trimmed.Substring($trimmed.Length - 4000) }
        $body = @"
$specBody

---

## 直前の試行が不合格だった（試行 $($attempt - 1)）

検証コマンド: ``$VerifyCommand``
終了コード: $($lastVerify.ExitCode)

出力（末尾）:

``````
$trimmed
``````

**この失敗を直すことだけに集中すること。** 指示書の「やらないこと」は引き続き厳守。
"@
    }
    Set-Content -LiteralPath $iterSpec -Value $body -Encoding UTF8

    $attemptDir = Join-Path $loopDir ("attempt-{0:d2}" -f $attempt)
    $dispatchArgs = @{
        SpecPath       = $iterSpec
        WorkDir        = $workFull
        Effort         = $Effort
        TimeoutMinutes = $TimeoutMinutes
        RunDir         = $attemptDir
    }
    if ($Model)       { $dispatchArgs['Model'] = $Model }
    if ($AutoApprove) { $dispatchArgs['AutoApprove'] = $true }

    & $dispatcher @dispatchArgs
    $dispatchCode = $LASTEXITCODE

    if ($dispatchCode -eq 3) {
        Write-Warning "無料枠切れのため中断します（試行 $attempt で停止、上限 $MaxAttempts）。"
        $log.Add("試行 $attempt : 無料枠切れで中断")
        $verdict = 'QUOTA'
        break
    }
    if ($dispatchCode -eq 2) {
        Write-Warning "前提不足のため中断します。"
        $log.Add("試行 $attempt : 前提不足で中断")
        $verdict = 'PRECONDITION'
        break
    }

    Write-Host "検証中: $VerifyCommand"
    $lastVerify = Invoke-Verify -Command $VerifyCommand -Directory $workFull
    Set-Content -LiteralPath (Join-Path $attemptDir 'verify.txt') `
        -Value "exit=$($lastVerify.ExitCode)`r`n`r`n$($lastVerify.Output)" -Encoding UTF8

    if ($lastVerify.ExitCode -eq 0) {
        Write-Host "合格（試行 $attempt）"
        $log.Add("試行 $attempt : 合格")
        $verdict = 'PASSED'
        break
    }

    Write-Host "不合格（exit $($lastVerify.ExitCode)）"
    $log.Add("試行 $attempt : 不合格 exit=$($lastVerify.ExitCode) / agy exit=$dispatchCode")
    Write-Host ""
}

Remove-Item -LiteralPath $iterSpec -Force -ErrorAction SilentlyContinue

# --- まとめ -------------------------------------------------------------
$summary = @"
# Antigravity ループ結果

- 日時: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
- 指示書: $specFull
- 作業先: $workFull
- 検証コマンド: ``$VerifyCommand``
- 使った試行: $used / $MaxAttempts
- 結果: **$verdict**

## 経過

$($log | ForEach-Object { "- $_" } | Out-String)

## 次にやること

$(switch ($verdict) {
    'PASSED'       { "Claude Codeが ``git diff`` をレビューしてcommitする。検証が通ったことと、意図どおりであることは別物。" }
    'QUOTA'        { "無料枠が戻ってから再投入する。急ぐならClaude Codeが自分でやる。" }
    'PRECONDITION' { "agyの導入・ログイン、指示書のパスを確認する。" }
    default        { "上限まで直せなかった。**指示書か検証コマンドを書き直す。** 同じものを投げ直さない。だいたい原因は完了条件の曖昧さか、検証が粗すぎること。" }
})
"@
Set-Content -LiteralPath (Join-Path $loopDir 'loop-summary.md') -Value $summary -Encoding UTF8

Write-Host ""
Write-Host "結果: $verdict（$used / $MaxAttempts 回）"
Write-Host "記録: $loopDir"

switch ($verdict) {
    'PASSED'       { exit 0 }
    'QUOTA'        { exit 3 }
    'PRECONDITION' { exit 2 }
    default        { exit 1 }
}
