<#
.SYNOPSIS
    スタートアップの start_chat_server.vbs（起動時エラー 80070002）を片付ける。

.DESCRIPTION
    2026-09-10 に Hermes-Pipeline → AI-Harness\hermes へ移動した際、
    スタートアップフォルダに置かれた「コピー」だけが旧パスを指したまま残り、
    PC起動時に「指定されたファイルが見つかりません（80070002）」が出ている。

    Delete   : スタートアップのコピーとデスクトップの「Hermesとチャット」を削除する（推奨）。
               チャットページが使う hermes3:8b は不採用モデルで、8/26以降使われていないため。
    Shortcut : 残す場合。コピーを消し、AI-Harness\hermes\start_chat_server.vbs への
               ショートカットを置き直す（以後フォルダを動かしてもショートカットだけ直せば済む）。

    削除・置換の前に、対象ファイルを AI-Harness\hermes\_backup へ退避する。

.EXAMPLE
    # まず何が起きるかだけ見る
    powershell -ExecutionPolicy Bypass -File .\Fix-StartupChatServer.ps1 -Mode Delete -DryRun

.EXAMPLE
    # 実行する
    powershell -ExecutionPolicy Bypass -File .\Fix-StartupChatServer.ps1 -Mode Delete
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('Delete', 'Shortcut')]
    [string]$Mode,

    [string]$HarnessRoot = "$env:USERPROFILE\AI-Harness",
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$hermes     = Join-Path $HarnessRoot 'hermes'
$source     = Join-Path $hermes 'start_chat_server.vbs'
$startupDir = [Environment]::GetFolderPath('Startup')
$desktopDir = [Environment]::GetFolderPath('Desktop')
$backupDir  = Join-Path $hermes '_backup'
$stamp      = Get-Date -Format 'yyyyMMdd-HHmmss'

function Do-Step {
    param([string]$Description, [scriptblock]$Action)
    if ($DryRun) {
        Write-Host "[DryRun] $Description"
    } else {
        Write-Host "[実行]   $Description"
        & $Action
    }
}

function Backup-File {
    param([string]$Path)
    if ($DryRun) { return }
    if (-not (Test-Path -LiteralPath $backupDir)) {
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    }
    $name = "$stamp-" + (Split-Path -Leaf $Path)
    Copy-Item -LiteralPath $Path -Destination (Join-Path $backupDir $name) -Force
}

if (-not $startupDir) {
    throw 'スタートアップフォルダを特定できませんでした。Windows上で実行してください。'
}

Write-Host "モード: $Mode$(if ($DryRun) { ' (DryRun — 変更しません)' })"
Write-Host "スタートアップ: $startupDir"
Write-Host ""

$touched = 0

# --- 1. スタートアップにある start_chat_server.vbs（旧パスを指すコピー） ---
$startupVbs = Join-Path $startupDir 'start_chat_server.vbs'
if (Test-Path -LiteralPath $startupVbs) {
    $body = Get-Content -LiteralPath $startupVbs -Raw -ErrorAction SilentlyContinue
    if ($body -and $body -match 'Hermes-Pipeline') {
        Write-Host "見つかりました（旧パスを指しています）: $startupVbs"
    } else {
        Write-Host "見つかりました: $startupVbs"
    }
    Do-Step "退避して削除: $startupVbs" {
        Backup-File $startupVbs
        Remove-Item -LiteralPath $startupVbs -Force
    }
    $touched++
} else {
    Write-Host "スタートアップに start_chat_server.vbs はありません（対処済みか、元からない）"
}

# --- 2. スタートアップの古いショートカット ---
$startupLnks = @()
if ($startupDir -and (Test-Path -LiteralPath $startupDir)) {
    $startupLnks = @(Get-ChildItem -LiteralPath $startupDir -Filter '*.lnk' -ErrorAction SilentlyContinue)
}
foreach ($lnk in $startupLnks) {
    try {
        $sh = New-Object -ComObject WScript.Shell
        $target = $sh.CreateShortcut($lnk.FullName).TargetPath
    } catch { continue }
    if ($target -and ($target -match 'Hermes-Pipeline' -or $target -match 'start_chat_server')) {
        if (-not (Test-Path -LiteralPath $target) -or $Mode -eq 'Delete') {
            Do-Step "スタートアップの古いショートカットを削除: $($lnk.Name)（参照先 $target）" {
                Remove-Item -LiteralPath $lnk.FullName -Force
            }
            $touched++
        }
    }
}

# --- 3. モード別の仕上げ ---
if ($Mode -eq 'Shortcut') {
    if (-not (Test-Path -LiteralPath $source)) {
        throw "本体が見つかりません: $source  （-HarnessRoot の指定を確認してください）"
    }
    $newLnk = Join-Path $startupDir 'start_chat_server.lnk'
    Do-Step "ショートカットを作成: $newLnk → $source" {
        $sh = New-Object -ComObject WScript.Shell
        $s = $sh.CreateShortcut($newLnk)
        $s.TargetPath       = $source
        $s.WorkingDirectory = $hermes
        $s.Description      = 'Hermes チャットページ用サーバー'
        $s.Save()
    }
    $touched++
} else {
    # Delete モード: デスクトップの「Hermesとチャット」も消す
    $desktopItems = @()
    if ($desktopDir -and (Test-Path -LiteralPath $desktopDir)) {
        $desktopItems = @(Get-ChildItem -LiteralPath $desktopDir -ErrorAction SilentlyContinue)
    }
    foreach ($item in @($desktopItems |
                        Where-Object { $_.BaseName -like '*Hermes*チャット*' -or $_.BaseName -like '*Hermesとチャット*' })) {
        Do-Step "デスクトップから削除: $($item.Name)" {
            Backup-File $item.FullName
            Remove-Item -LiteralPath $item.FullName -Force
        }
        $touched++
    }
}

Write-Host ""
if ($DryRun) {
    Write-Host "DryRun のため何も変更していません。対象は $touched 件。"
} elseif ($touched -eq 0) {
    Write-Host "対象がありませんでした。すでに片付いています。"
} else {
    Write-Host "$touched 件を処理しました。退避先: $backupDir"
    Write-Host "次回のPC起動でエラー80070002が出なければ完了です。"
}

exit 0
