<#
.SYNOPSIS
    AI-Harness（自宅PC自動化）の健康診断。読み取りのみで、何も変更しない。

.DESCRIPTION
    Notion「自宅PC自動化 運用カード」に記載された5か所のパス依存と、
    自動取込パイプラインが生きているかを一度に確認する。
    自動取込は壊れても黙って止まるため、定期的にこれを流して状態を見る。

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\Check-Harness.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\Check-Harness.ps1 -ReportPath "$env:USERPROFILE\Desktop\harness-report.md"
#>
[CmdletBinding()]
param(
    [string]$HarnessRoot = "$env:USERPROFILE\AI-Harness",
    [string]$ReportPath
)

$ErrorActionPreference = 'Continue'
$lines = New-Object System.Collections.Generic.List[string]
$problems = New-Object System.Collections.Generic.List[string]

function Add-Line { param([string]$Text) $lines.Add($Text) | Out-Null; Write-Host $Text }
function Add-Problem { param([string]$Text) $problems.Add($Text) | Out-Null }

$hermes      = Join-Path $HarnessRoot 'hermes'
$startupDir  = [Environment]::GetFolderPath('Startup')
$desktopDir  = [Environment]::GetFolderPath('Desktop')
$taskName    = 'HermesPipeline_DriveSync'

Add-Line "# AI-Harness 健康診断"
Add-Line ""
Add-Line "実行日時: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Add-Line "対象: ``$HarnessRoot``"
Add-Line ""

# --- 1. フォルダ ---------------------------------------------------------
Add-Line "## 1. フォルダ"
foreach ($p in @($HarnessRoot, $hermes)) {
    if (Test-Path -LiteralPath $p) {
        Add-Line "- OK   $p"
    } else {
        Add-Line "- NG   $p （見つからない）"
        Add-Problem "フォルダが見つからない: $p"
    }
}
if ($env:USERPROFILE) {
    $bak = Join-Path $env:USERPROFILE 'Hermes-Pipeline.bak-20260910'
    if (Test-Path -LiteralPath $bak) {
        Add-Line "- 参考 旧フォルダのバックアップが残っている: $bak"
    }
}
Add-Line ""

# --- 2. タスクスケジューラ ----------------------------------------------
Add-Line "## 2. タスクスケジューラ（$taskName）"
$task = $null
if (Get-Command Get-ScheduledTask -ErrorAction SilentlyContinue) {
    $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
} else {
    Add-Line "- 確認不可 このOSにはタスクスケジューラのコマンドがない（Windowsで実行してください）"
}
if (-not $task) {
    Add-Line "- NG   タスクが登録されていない。自動取込は動いていない。"
    Add-Problem "タスク $taskName が存在しない"
} else {
    Add-Line "- 状態: $($task.State)"
    if ($task.State -eq 'Disabled') { Add-Problem "タスク $taskName が無効になっている" }

    $info = Get-ScheduledTaskInfo -TaskName $taskName -ErrorAction SilentlyContinue
    if ($info) {
        Add-Line "- 前回実行: $($info.LastRunTime)  結果コード: $($info.LastTaskResult)"
        Add-Line "- 次回実行: $($info.NextRunTime)"
        if ($info.LastTaskResult -ne 0) {
            Add-Problem "タスク $taskName の前回実行が失敗している（結果コード $($info.LastTaskResult)）"
        }
        if ($info.LastRunTime -and $info.LastRunTime -lt (Get-Date).AddHours(-6)) {
            Add-Problem "タスク $taskName が6時間以上動いていない（3時間おきのはず）"
        }
    }

    foreach ($a in $task.Actions) {
        $exe = $a.Execute
        $arg = $a.Arguments
        $wd  = $a.WorkingDirectory
        Add-Line "- 実行: $exe $arg"
        if ($wd) { Add-Line "- 作業フォルダ: $wd" }
        foreach ($ref in @($exe, $arg, $wd)) {
            if ($ref -and $ref -match 'Hermes-Pipeline') {
                Add-Line "  NG  旧パス（Hermes-Pipeline）を指している"
                Add-Problem "タスク $taskName が旧パス Hermes-Pipeline を指している"
            }
        }
        if ($wd -and -not (Test-Path -LiteralPath $wd)) {
            Add-Problem "タスク $taskName の作業フォルダが存在しない: $wd"
        }
    }
}
Add-Line ""

# --- 3. スタートアップ ---------------------------------------------------
Add-Line "## 3. スタートアップフォルダ"
Add-Line "場所: ``$startupDir``"
$startupItems = @()
if ($startupDir -and (Test-Path -LiteralPath $startupDir)) {
    $startupItems = @(Get-ChildItem -LiteralPath $startupDir -ErrorAction SilentlyContinue)
}
if ($startupItems.Count -eq 0) {
    Add-Line "- 登録なし"
} else {
    foreach ($item in $startupItems) {
        Add-Line "- $($item.Name)"
        if ($item.Extension -eq '.vbs') {
            $body = Get-Content -LiteralPath $item.FullName -Raw -ErrorAction SilentlyContinue
            if ($body -and $body -match 'Hermes-Pipeline') {
                Add-Line "  NG  中身が旧パス（Hermes-Pipeline）を指している → 起動時エラー80070002の原因"
                Add-Problem "スタートアップの $($item.Name) が旧パスを指している（Fix-StartupChatServer.ps1 で対処）"
            }
        }
        if ($item.Extension -eq '.lnk') {
            try {
                $sh = New-Object -ComObject WScript.Shell
                $lnk = $sh.CreateShortcut($item.FullName)
                Add-Line "  参照先: $($lnk.TargetPath)"
                if ($lnk.TargetPath -and -not (Test-Path -LiteralPath $lnk.TargetPath)) {
                    Add-Line "  NG  参照先が存在しない"
                    Add-Problem "スタートアップのショートカット $($item.Name) の参照先が存在しない"
                }
            } catch { Add-Line "  （ショートカットを読めなかった）" }
        }
    }
}
Add-Line ""

# --- 4. hermes 配下の .vbs（文字コード） --------------------------------
Add-Line "## 4. hermes 配下の .vbs（日本語コメント入りは UTF-16LE BOM 必須）"
if (Test-Path -LiteralPath $hermes) {
    $vbs = @(Get-ChildItem -LiteralPath $hermes -Filter '*.vbs' -ErrorAction SilentlyContinue)
    if ($vbs.Count -eq 0) { Add-Line "- .vbs なし" }
    foreach ($f in $vbs) {
        $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
        $enc = 'その他/UTF-8(BOMなし)'
        if     ($bytes.Length -ge 2 -and $bytes[0] -eq 0xFF -and $bytes[1] -eq 0xFE) { $enc = 'UTF-16LE BOM付き' }
        elseif ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) { $enc = 'UTF-8 BOM付き' }
        $mark = if ($enc -eq 'UTF-16LE BOM付き') { 'OK  ' } else { '注意' }
        Add-Line "- $mark $($f.Name) : $enc"
        if ($enc -ne 'UTF-16LE BOM付き') {
            $raw = Get-Content -LiteralPath $f.FullName -Raw -ErrorAction SilentlyContinue
            if ($raw -match '[^\x00-\x7F]') {
                Add-Problem "$($f.Name) は日本語を含むのに UTF-16LE BOM付き ではない（WSHエラーの原因になる）"
            }
        }
        $body = Get-Content -LiteralPath $f.FullName -Raw -ErrorAction SilentlyContinue
        if ($body -and $body -match 'Hermes-Pipeline') {
            Add-Problem "$($f.Name) が旧パス Hermes-Pipeline を指している"
        }
    }
} else {
    Add-Line "- hermes フォルダがないため確認できない"
}
Add-Line ""

# --- 5. ログ -------------------------------------------------------------
Add-Line "## 5. 取込ログ（startup_sync.log）"
$log = Join-Path $hermes 'startup_sync.log'
if (Test-Path -LiteralPath $log) {
    $li = Get-Item -LiteralPath $log
    Add-Line "- 最終更新: $($li.LastWriteTime)  サイズ: $([math]::Round($li.Length/1KB,1)) KB"
    if ($li.LastWriteTime -lt (Get-Date).AddDays(-1)) {
        Add-Problem "startup_sync.log が24時間以上更新されていない（取込が止まっている疑い）"
    }
    Add-Line ""
    Add-Line '```'
    Get-Content -LiteralPath $log -Tail 20 -ErrorAction SilentlyContinue | ForEach-Object { Add-Line $_ }
    Add-Line '```'
} else {
    Add-Line "- NG   ログがない: $log"
    Add-Problem "startup_sync.log が存在しない（取込が一度も動いていない可能性）"
}
Add-Line ""

# --- 6. 常駐プロセス -----------------------------------------------------
Add-Line "## 6. 常駐しているはずのもの"
$want = @(
    @{ Name = 'Obsidian'; Proc = 'Obsidian'; Note = 'これが起動していないと取込は動かない' },
    @{ Name = 'Ollama';   Proc = 'ollama';   Note = 'ローカルLLMの土台' },
    @{ Name = 'Hermes Desktop'; Proc = 'Hermes'; Note = 'Discord経由のHermes' }
)
foreach ($w in $want) {
    $p = Get-Process -Name $w.Proc -ErrorAction SilentlyContinue
    if ($p) {
        Add-Line "- OK   $($w.Name)（PID: $(($p | Select-Object -First 1).Id)）"
    } else {
        Add-Line "- 停止 $($w.Name) — $($w.Note)"
        if ($w.Proc -eq 'Obsidian') { Add-Problem "Obsidian が起動していない（取込が動かない）" }
    }
}
Add-Line ""

# --- まとめ --------------------------------------------------------------
Add-Line "## まとめ"
if ($problems.Count -eq 0) {
    Add-Line "問題なし。"
} else {
    Add-Line "$($problems.Count) 件の要対応:"
    $i = 1
    foreach ($p in $problems) { Add-Line "$i. $p"; $i++ }
}

if ($ReportPath) {
    $lines -join "`r`n" | Set-Content -LiteralPath $ReportPath -Encoding UTF8
    Write-Host ""
    Write-Host "レポートを保存しました: $ReportPath"
}

exit 0
