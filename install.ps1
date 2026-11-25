<#
.SYNOPSIS
    Установщик темы Discord Classic Dark для TeamSpeak 6 (v2.0).

.DESCRIPTION
    Устанавливает расширение dev.custom.discord в TeamSpeak 6 и позволяет
    выбрать один из 6 вариантов темы (лента 72px / широкая панель, с баннерами каналов и без),
    а также автоматически активирует выбранный вариант в settings.db.

.PARAMETER Preset
    Номер варианта:
      1 = Discord Dark (72px + закладки/чаты, без баннеров)
      2 = Discord Dark + Banners (72px + закладки/чаты + баннеры каналов)
      3 = Discord Rail (минимальная лента 72px, без баннеров)
      4 = Discord Rail + Banners (минимальная лента 72px + баннеры каналов)
      5 = Discord Wide (широкая левая панель, без баннеров)
      6 = Discord Wide + Banners (широкая левая панель + баннеры каналов)
      7 = Установить без изменения активной темы
      8 = Удалить тему (сброс на стандартную)

.PARAMETER ProfileName
    Имя папки профиля TeamSpeak в %APPDATA%\TeamSpeak (по умолчанию: Default или выбор из списка).

.PARAMETER SourceDir
    Локальный путь к папке extension\ (по умолчанию определяется автоматически рядом со скриптом).

.PARAMETER RepoArchiveUrl
    URL ZIP-архива GitHub-репозитория при удалённом запуске (irm ... | iex).

.PARAMETER AutoRestart
    Автоматически закрывать (корректно с сохранением WAL) и перезапускать TeamSpeak 6.

.PARAMETER NoRestart
    Не закрывать и не перезапускать запущенный TeamSpeak 6.

.PARAMETER Uninstall
    Удалить установленное расширение и сбросить тему в settings.db.

.EXAMPLE
    .\install.ps1
    .\install.ps1 -Preset 4 -AutoRestart
    .\install.ps1 -Uninstall -AutoRestart
#>

[CmdletBinding()]
param(
    [ValidateRange(0, 8)]
    [int]$Preset = 0,
    [string]$ProfileName = "",
    [string]$SourceDir = "",
    [string]$RepoArchiveUrl = "",
    [switch]$AutoRestart,
    [switch]$NoRestart,
    [switch]$Uninstall
)

# GitHub-репозиторий для удалённой установки (irm ... | iex):
$DefaultRepoSlug = "Roskud/teamspeak6-discord-theme"
$ExtId = "dev.custom.discord"

$Presets = [ordered]@{
    "1" = @{ Name = "Discord Dark";            File = "discord.css";              Tag = "Лента 72px + закладки/чаты (без баннеров)" }
    "2" = @{ Name = "Discord Dark + Banners";  File = "discord-banners.css";      Tag = "Лента 72px + закладки/чаты + баннеры" }
    "3" = @{ Name = "Discord Rail";            File = "discord-rail.css";         Tag = "Лента 72px (скрыты чаты/контакты в звонке, без баннеров)" }
    "4" = @{ Name = "Discord Rail + Banners";  File = "discord-rail-banners.css"; Tag = "Рекомендуется: лента 72px + баннеры каналов (без чатов)" }
    "5" = @{ Name = "Discord Wide";            File = "discord-wide.css";         Tag = "Широкая левая панель (без баннеров)" }
    "6" = @{ Name = "Discord Wide + Banners";  File = "discord-wide-banners.css"; Tag = "Широкая левая панель + баннеры" }
    "7" = @{ Name = "Только установить файлы"; File = "";                         Tag = "Установить 6 стилей без изменения settings.db" }
    "8" = @{ Name = "Удалить тему";            File = "";                         Tag = "Удалить dev.custom.discord и сбросить стиль" }
}

function Write-Color {
    param(
        [string]$Text,
        [ConsoleColor]$Color = [ConsoleColor]::Gray,
        [switch]$NoNewline
    )
    Write-Host $Text -ForegroundColor $Color -NoNewline:$NoNewline
}

function Show-Banner {
    Clear-Host
    Write-Color "====================================================================`n" "Cyan"
    Write-Color "   Discord Classic Dark для TeamSpeak 6 — Установщик темы (v2.0)`n" "White"
    Write-Color "====================================================================`n`n" "Cyan"
}

function Find-TeamSpeakProfiles {
    $tsRoot = Join-Path $env:APPDATA "TeamSpeak"
    $found = @()
    if (Test-Path $tsRoot) {
        $dirs = Get-ChildItem -Path $tsRoot -Directory -ErrorAction SilentlyContinue
        foreach ($d in $dirs) {
            if ((Test-Path (Join-Path $d.FullName "settings.db")) -or (Test-Path (Join-Path $d.FullName "extensions"))) {
                $found += $d.FullName
            }
        }
    }
    return ,$found
}

function Select-TargetProfile {
    param(
        [string[]]$Profiles,
        [string]$RequestedName,
        [bool]$AllowInteractive
    )
    if (-not $Profiles -or $Profiles.Count -eq 0) {
        if (-not [string]::IsNullOrWhiteSpace($RequestedName)) {
            throw "Профиль TeamSpeak '$RequestedName' не найден в $(Join-Path $env:APPDATA 'TeamSpeak')."
        }
        return (Join-Path $env:APPDATA "TeamSpeak\Default")
    }

    if (-not [string]::IsNullOrWhiteSpace($RequestedName)) {
        $match = $Profiles | Where-Object { (Split-Path $_ -Leaf) -ieq $RequestedName } | Select-Object -First 1
        if (-not $match) {
            $avail = ($Profiles | ForEach-Object { Split-Path $_ -Leaf }) -join ", "
            throw "Профиль TeamSpeak '$RequestedName' не найден. Доступные профили: $avail"
        }
        return $match
    }

    if ($Profiles.Count -eq 1) {
        return $Profiles[0]
    }

    $def = $Profiles | Where-Object { (Split-Path $_ -Leaf) -ieq "Default" } | Select-Object -First 1
    if ($AllowInteractive) {
        Write-Color "Найдено несколько профилей TeamSpeak:`n" "White"
        for ($i = 0; $i -lt $Profiles.Count; $i++) {
            $leaf = Split-Path $Profiles[$i] -Leaf
            Write-Color ("  [{0}] " -f ($i + 1)) "Cyan" -NoNewline
            Write-Color "$leaf " "White" -NoNewline
            Write-Color "($($Profiles[$i]))`n" "DarkGray"
        }
        $ans = Read-Host "Выберите профиль [1-$($Profiles.Count)] (Enter = 1)"
        if ([string]::IsNullOrWhiteSpace($ans)) {
            return $(if ($def) { $def } else { $Profiles[0] })
        }
        $idx = 0
        if ([int]::TryParse($ans.Trim(), [ref]$idx) -and $idx -ge 1 -and $idx -le $Profiles.Count) {
            return $Profiles[$idx - 1]
        }
        throw "Некорректный выбор профиля: $ans"
    }

    return $(if ($def) { $def } else { $Profiles[0] })
}

function Find-TeamSpeakExe {
    $candidates = @()
    $running = Get-Process -Name "TeamSpeak" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($running) {
        try {
            if (-not [string]::IsNullOrWhiteSpace($running.Path)) {
                $candidates += $running.Path
            }
        } catch {}
    }

    $candidates += @(
        (Join-Path $env:LOCALAPPDATA "Programs\TeamSpeak\TeamSpeak.exe"),
        (Join-Path $env:ProgramFiles "TeamSpeak\TeamSpeak.exe")
    )
    if (-not [string]::IsNullOrWhiteSpace(${env:ProgramFiles(x86)})) {
        $candidates += (Join-Path ${env:ProgramFiles(x86)} "TeamSpeak\TeamSpeak.exe")
    }

    $appPaths = @(
        "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\TeamSpeak.exe",
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\TeamSpeak.exe"
    )
    foreach ($reg in $appPaths) {
        if (Test-Path $reg) {
            $val = (Get-ItemProperty $reg -ErrorAction SilentlyContinue).'(default)'
            if ($val) { $candidates += $val }
        }
    }

    foreach ($p in $candidates) {
        if ($p -and (Test-Path $p)) { return $p }
    }
    return $null
}

function Ensure-WinSqliteType {
    if ("TSWinSqlite" -as [type]) { return $true }
    $winsqlite = Join-Path $env:SystemRoot "System32\winsqlite3.dll"
    if (-not (Test-Path $winsqlite)) { return $false }

    Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Text;

public static class TSWinSqlite {
    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_open_v2(string filename, out IntPtr ppDb, int flags, IntPtr zVfs);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_close_v2(IntPtr db);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_exec(IntPtr db, string sql, IntPtr cb, IntPtr arg, out IntPtr errMsg);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern void sqlite3_free(IntPtr ptr);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_prepare_v2(IntPtr db, string zSql, int nByte, out IntPtr ppStmt, out IntPtr pzTail);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_bind_text(IntPtr pStmt, int idx, byte[] val, int n, IntPtr freeFn);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_step(IntPtr pStmt);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_finalize(IntPtr pStmt);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern IntPtr sqlite3_column_text(IntPtr pStmt, int iCol);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_column_bytes(IntPtr pStmt, int iCol);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern IntPtr sqlite3_errmsg(IntPtr db);

    private static string GetError(IntPtr db) {
        if (db == IntPtr.Zero) return "unknown sqlite error";
        return Marshal.PtrToStringAnsi(sqlite3_errmsg(db)) ?? "sqlite error";
    }

    public static void CheckpointTruncate(string dbPath) {
        IntPtr db = IntPtr.Zero;
        try {
            int rc = sqlite3_open_v2(dbPath, out db, 2, IntPtr.Zero);
            if (rc != 0) throw new Exception("sqlite3_open_v2 failed (" + rc + "): " + GetError(db));
            IntPtr errPtr;
            rc = sqlite3_exec(db, "PRAGMA busy_timeout=3000; PRAGMA wal_checkpoint(TRUNCATE);", IntPtr.Zero, IntPtr.Zero, out errPtr);
            if (errPtr != IntPtr.Zero) sqlite3_free(errPtr);
            if (rc != 0) throw new Exception("wal_checkpoint failed (" + rc + "): " + GetError(db));
        } finally {
            if (db != IntPtr.Zero) sqlite3_close_v2(db);
        }
    }

    public static string ReadGeneralSettings(string dbPath) {
        IntPtr db = IntPtr.Zero;
        IntPtr stmt = IntPtr.Zero;
        try {
            int rc = sqlite3_open_v2(dbPath, out db, 1, IntPtr.Zero);
            if (rc != 0) throw new Exception("sqlite3_open_v2 failed (" + rc + "): " + GetError(db));
            IntPtr tail;
            rc = sqlite3_prepare_v2(db, "SELECT value FROM json_blobs WHERE key='general_settings' LIMIT 1;", -1, out stmt, out tail);
            if (rc != 0) throw new Exception("sqlite3_prepare_v2 failed (" + rc + "): " + GetError(db));
            rc = sqlite3_step(stmt);
            if (rc == 101) return null; // SQLITE_DONE (row not found)
            if (rc != 100) throw new Exception("sqlite3_step failed (" + rc + "): " + GetError(db));
            IntPtr ptr = sqlite3_column_text(stmt, 0);
            int len = sqlite3_column_bytes(stmt, 0);
            if (ptr == IntPtr.Zero || len <= 0) return null;
            byte[] buf = new byte[len];
            Marshal.Copy(ptr, buf, 0, len);
            return Encoding.UTF8.GetString(buf);
        } finally {
            if (stmt != IntPtr.Zero) sqlite3_finalize(stmt);
            if (db != IntPtr.Zero) sqlite3_close_v2(db);
        }
    }

    public static void WriteGeneralSettings(string dbPath, string jsonText) {
        IntPtr db = IntPtr.Zero;
        IntPtr stmt = IntPtr.Zero;
        try {
            int rc = sqlite3_open_v2(dbPath, out db, 2, IntPtr.Zero);
            if (rc != 0) throw new Exception("sqlite3_open_v2 failed (" + rc + "): " + GetError(db));
            IntPtr errPtr;
            sqlite3_exec(db, "PRAGMA busy_timeout=3000;", IntPtr.Zero, IntPtr.Zero, out errPtr);
            if (errPtr != IntPtr.Zero) sqlite3_free(errPtr);

            IntPtr tail;
            rc = sqlite3_prepare_v2(db, "UPDATE json_blobs SET value = ?1, timestamp = COALESCE(timestamp + 1, 0) WHERE key = 'general_settings';", -1, out stmt, out tail);
            if (rc != 0) throw new Exception("sqlite3_prepare_v2 failed (" + rc + "): " + GetError(db));
            byte[] utf8 = Encoding.UTF8.GetBytes(jsonText);
            rc = sqlite3_bind_text(stmt, 1, utf8, utf8.Length, new IntPtr(-1));
            if (rc != 0) throw new Exception("sqlite3_bind_text failed (" + rc + "): " + GetError(db));
            rc = sqlite3_step(stmt);
            if (rc != 101) throw new Exception("sqlite3_step failed (" + rc + "): " + GetError(db));
            rc = sqlite3_exec(db, "PRAGMA wal_checkpoint(TRUNCATE);", IntPtr.Zero, IntPtr.Zero, out errPtr);
            if (errPtr != IntPtr.Zero) sqlite3_free(errPtr);
        } finally {
            if (stmt != IntPtr.Zero) sqlite3_finalize(stmt);
            if (db != IntPtr.Zero) sqlite3_close_v2(db);
        }
    }
}
"@
    return $true
}

function Set-JsonProp {
    param(
        [psobject]$Target,
        [string]$Name,
        $Value
    )
    $Target | Add-Member -MemberType NoteProperty -Name $Name -Value $Value -Force
}

function Ensure-JsonSubObject {
    param(
        [psobject]$Parent,
        [string]$Name
    )
    $prop = $Parent.PSObject.Properties[$Name]
    if (-not $prop -or $null -eq $prop.Value -or ($prop.Value -isnot [pscustomobject])) {
        $sub = [pscustomobject]@{}
        $Parent | Add-Member -MemberType NoteProperty -Name $Name -Value $sub -Force
        return $sub
    }
    return $prop.Value
}

function Update-SettingsDb {
    param(
        [string]$SettingsDbPath,
        [string]$StyleName
    )
    if (-not (Test-Path $SettingsDbPath)) { return $false }
    if (-not (Ensure-WinSqliteType)) { return $false }

    # Checkpoint WAL first so settings.db and its backup include all latest writes
    [TSWinSqlite]::CheckpointTruncate($SettingsDbPath)
    $raw = [TSWinSqlite]::ReadGeneralSettings($SettingsDbPath)
    if ([string]::IsNullOrWhiteSpace($raw)) { return $false }

    $obj = $raw | ConvertFrom-Json
    $appearance = Ensure-JsonSubObject -Parent $obj -Name "appearance"
    $workflow = Ensure-JsonSubObject -Parent $obj -Name "workflow"

    if ([string]::IsNullOrEmpty($StyleName)) {
        if ($appearance.PSObject.Properties['user_style']) {
            $appearance.PSObject.Properties.Remove('user_style')
        }
        Set-JsonProp -Target $workflow -Name "keepActiveItemsInList" -Value $true
    } else {
        # Always allow TS6 to expose banner assets so all 6 theme variants work smoothly without reinstall
        Set-JsonProp -Target $appearance -Name "user_style" -Value $StyleName
        Set-JsonProp -Target $appearance -Name "show_servertree_channel_banners" -Value $true
        # Prevent active connected server from duplicating in Bookmarks while keeping other saved servers clickable
        Set-JsonProp -Target $workflow -Name "keepActiveItemsInList" -Value $false
    }

    $bakPath = "$SettingsDbPath.bak"
    Copy-Item -Path $SettingsDbPath -Destination $bakPath -Force

    $newJson = $obj | ConvertTo-Json -Depth 32 -Compress
    # Restore JavaScriptSerializer HTML-escaped chars on PS 5.1 if present
    $newJson = $newJson -replace '\\u003c', '<' -replace '\\u003e', '>' -replace '\\u0026', '&' -replace '\\u0027', "'"
    [TSWinSqlite]::WriteGeneralSettings($SettingsDbPath, $newJson)
    return $true
}

function Resolve-ExtensionSource {
    param(
        [string]$ExplicitSource,
        [string]$ArchiveUrl,
        [string]$TempRoot
    )

    if ($ExplicitSource -and (Test-Path (Join-Path $ExplicitSource "package.json"))) {
        return $ExplicitSource
    }

    if ($PSScriptRoot) {
        $localExt = Join-Path $PSScriptRoot "extension"
        if (Test-Path (Join-Path $localExt "package.json")) {
            return $localExt
        }
    }

    $cwdExt = Join-Path (Get-Location).Path "extension"
    if (Test-Path (Join-Path $cwdExt "package.json")) {
        return $cwdExt
    }

    if (-not $ArchiveUrl) {
        if ($DefaultRepoSlug -match '<USER>|<REPO>') {
            throw "Локальная папка 'extension' не найдена, а URL GitHub-репозитория ещё не настроен. Запустите install.ps1 из клонированного репозитория или передайте -RepoArchiveUrl <zip_url>."
        }
        $ArchiveUrl = "https://github.com/$DefaultRepoSlug/archive/refs/heads/main.zip"
    }

    Write-Color "-> Скачиваю тему из GitHub...`n" "Cyan"
    New-Item -ItemType Directory -Path $TempRoot -Force | Out-Null
    $zipPath = Join-Path $TempRoot "repo.zip"
    $extractPath = Join-Path $TempRoot "extracted"

    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
    } catch {}

    if ($PSVersionTable.PSVersion.Major -lt 6) {
        Invoke-WebRequest -Uri $ArchiveUrl -OutFile $zipPath -UseBasicParsing
    } else {
        Invoke-WebRequest -Uri $ArchiveUrl -OutFile $zipPath
    }
    Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force

    $pkg = Get-ChildItem -Path $extractPath -Filter "package.json" -Recurse | Where-Object {
        $_.DirectoryName -match 'extension$'
    } | Select-Object -First 1

    if (-not $pkg) {
        throw "Не удалось найти extension/package.json в скачанном архиве!"
    }
    return $pkg.DirectoryName
}

function Stop-TeamSpeakSafely {
    param([int]$TimeoutSeconds = 6)

    $procs = @(Get-Process -Name "TeamSpeak" -ErrorAction SilentlyContinue)
    if ($procs.Count -eq 0) { return }

    foreach ($p in $procs) {
        try {
            if ($p.MainWindowHandle -ne [IntPtr]::Zero) {
                [void]$p.CloseMainWindow()
            }
        } catch {}
    }

    $deadline = (Get-Date).AddSeconds(3)
    while ((Get-Date) -lt $deadline) {
        if (-not (Get-Process -Name "TeamSpeak" -ErrorAction SilentlyContinue)) { return }
        Start-Sleep -Milliseconds 250
    }

    Get-Process -Name "TeamSpeak" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    $hardDeadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $hardDeadline) {
        if (-not (Get-Process -Name "TeamSpeak" -ErrorAction SilentlyContinue)) { return }
        Start-Sleep -Milliseconds 250
    }
    throw "Не удалось корректно завершить процесс TeamSpeak.exe за отведённое время."
}

function Invoke-InstallerMain {
    $activePreset = $Preset
    if ($Uninstall) {
        if ($Preset -ne 0 -and $Preset -ne 8) {
            Write-Color "[i] Флаг -Uninstall имеет приоритет над -Preset $Preset.`n" "Yellow"
        }
        $activePreset = 8
    }

    $profiles = Find-TeamSpeakProfiles
    $interactiveMode = ($activePreset -eq 0)
    $targetProfile = Select-TargetProfile -Profiles $profiles -RequestedName $ProfileName -AllowInteractive:$interactiveMode
    $extTargetDir = Join-Path $targetProfile "extensions\$ExtId"
    $settingsDb = Join-Path $targetProfile "settings.db"

    if ($interactiveMode) {
        Show-Banner
        Write-Color "Профиль TeamSpeak: " "DarkGray" -NoNewline
        Write-Color "$targetProfile`n`n" "White"
        Write-Color "Выберите вариант темы Discord Classic Dark:`n`n" "White"

        foreach ($k in $Presets.Keys) {
            $p = $Presets[$k]
            $numColor = if ($k -eq "4") { "Green" } elseif ($k -eq "8") { "Red" } else { "Cyan" }
            Write-Color ("  [{0}] " -f $k) $numColor -NoNewline
            Write-Color ("{0,-24}" -f $p.Name) "White" -NoNewline
            Write-Color " — $($p.Tag)`n" "DarkGray"
        }
        Write-Color "`n  [Q] " "DarkGray" -NoNewline
        Write-Color "Выход`n`n" "DarkGray"

        while ($true) {
            $choice = Read-Host "Введите номер [1-8] (Enter = 4: Discord Rail + Banners)"
            if ([string]::IsNullOrWhiteSpace($choice)) {
                $activePreset = 4
                break
            }
            if ($choice.Trim().ToUpper() -eq "Q") {
                Write-Color "`nОтменено пользователем.`n" "Yellow"
                return
            }
            $parsed = 0
            if ([int]::TryParse($choice.Trim(), [ref]$parsed) -and $Presets.Contains("$parsed")) {
                $activePreset = $parsed
                break
            }
            Write-Color "Некорректный выбор. Введите число от 1 до 8 или Q.`n" "Red"
        }
        Write-Host ""
    }

    $selected = $Presets["$activePreset"]
    Write-Color "Выбран вариант: " "White" -NoNewline
    Write-Color "$($selected.Name)`n" "Cyan"

    # Capture TS6 executable BEFORE stopping so custom installation directories restart cleanly
    $tsExePath = Find-TeamSpeakExe
    $tempRoot = Join-Path $env:TEMP ("ts6-discord-install-" + [guid]::NewGuid().ToString("N"))

    try {
        # Validate/download extension source BEFORE closing running TeamSpeak
        $srcDir = $null
        if ($activePreset -ne 8) {
            $srcDir = Resolve-ExtensionSource -ExplicitSource $SourceDir -ArchiveUrl $RepoArchiveUrl -TempRoot $tempRoot
        }

        $tsRunning = @(Get-Process -Name "TeamSpeak" -ErrorAction SilentlyContinue)
        $shouldRestart = $false
        if ($tsRunning.Count -gt 0 -and -not $NoRestart) {
            if ($AutoRestart) {
                $shouldRestart = $true
            } else {
                $ans = Read-Host "TeamSpeak 6 сейчас запущен. Закрыть для чистой установки и перезапустить? [Y/n]"
                if ([string]::IsNullOrWhiteSpace($ans) -or $ans.Trim().ToLower().StartsWith("y")) {
                    $shouldRestart = $true
                }
            }
        }

        if ($shouldRestart) {
            Write-Color "-> Корректно закрываю TeamSpeak 6...`n" "DarkGray"
            Stop-TeamSpeakSafely
        } elseif ($tsRunning.Count -gt 0 -and $activePreset -ne 7) {
            Write-Color "   [!] TeamSpeak 6 всё ещё запущен — при сохранении settings.db перезапустите клиент вручную.`n" "Yellow"
        }

        if ($activePreset -eq 8) {
            if (Test-Path $extTargetDir) {
                Remove-Item -Path $extTargetDir -Recurse -Force
                Write-Color "[OK] Удалена папка расширения: $extTargetDir`n" "Green"
            } else {
                Write-Color "[i] Расширение не было установлено.`n" "Yellow"
            }
            if (Test-Path $settingsDb) {
                try {
                    if (Update-SettingsDb -SettingsDbPath $settingsDb -StyleName "") {
                        Write-Color "[OK] Активная тема сброшена на стандартную в settings.db`n" "Green"
                    }
                } catch {
                    Write-Color "   [!] Не удалось автоматически обновить settings.db: $($_.Exception.Message)`n" "Yellow"
                }
            }
        } else {
            New-Item -ItemType Directory -Path (Split-Path $extTargetDir -Parent) -Force | Out-Null
            if (Test-Path $extTargetDir) {
                Remove-Item -Path $extTargetDir -Recurse -Force
            }
            Copy-Item -Path $srcDir -Destination $extTargetDir -Recurse -Force
            Write-Color "[OK] Скопированы все 6 вариантов темы в: $extTargetDir`n" "Green"

            if ($activePreset -ge 1 -and $activePreset -le 6) {
                $styleName = $selected.Name
                $styleId = "$ExtId//$styleName"
                $dbOk = $false
                try {
                    $dbOk = Update-SettingsDb -SettingsDbPath $settingsDb -StyleName $styleId
                } catch {
                    Write-Color "   [!] Не удалось автоматически обновить settings.db: $($_.Exception.Message)`n" "Yellow"
                }
                if ($dbOk) {
                    Write-Color "[OK] Активирована тема '$styleName' и настроены каналы/серверы в settings.db (бэкап: settings.db.bak)`n" "Green"
                } else {
                    Write-Color "[i] Откройте TeamSpeak 6 -> Settings -> Appearance -> Theme и выберите '$styleName'`n" "Yellow"
                }
            }
        }

        if ($shouldRestart) {
            if ($tsExePath -and (Test-Path $tsExePath)) {
                Write-Color "-> Запускаю TeamSpeak 6...`n" "Cyan"
                Start-Process -FilePath $tsExePath
            } else {
                Write-Color "[i] Не найден TeamSpeak.exe — запустите TeamSpeak 6 вручную.`n" "Yellow"
            }
        } elseif ($tsRunning.Count -eq 0 -and -not $NoRestart) {
            if ($tsExePath -and (Test-Path $tsExePath)) {
                $shouldLaunchNow = $false
                if ($AutoRestart) {
                    $shouldLaunchNow = $true
                } else {
                    $launch = Read-Host "Запустить TeamSpeak 6 сейчас? [Y/n]"
                    if ([string]::IsNullOrWhiteSpace($launch) -or $launch.Trim().ToLower().StartsWith("y")) {
                        $shouldLaunchNow = $true
                    }
                }
                if ($shouldLaunchNow) {
                    Start-Process -FilePath $tsExePath
                }
            }
        }

        Write-Color "`nГотово! " "Green"
        if ($activePreset -eq 8) {
            Write-Color "Тема Discord Classic Dark удалена.`n" "Gray"
        } else {
            Write-Color "Все 6 вариантов всегда можно переключать в TeamSpeak 6: Settings -> Appearance -> Theme.`n" "Gray"
        }
    } finally {
        if (Test-Path $tempRoot) {
            Remove-Item -Path $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}

$__prevEap = $ErrorActionPreference
$__prevOutEnc = [Console]::OutputEncoding
$__prevInEnc = [Console]::InputEncoding
try {
    $ErrorActionPreference = "Stop"
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    [Console]::InputEncoding = [System.Text.Encoding]::UTF8
    Invoke-InstallerMain
} finally {
    $ErrorActionPreference = $__prevEap
    try { [Console]::OutputEncoding = $__prevOutEnc } catch {}
    try { [Console]::InputEncoding = $__prevInEnc } catch {}
}
