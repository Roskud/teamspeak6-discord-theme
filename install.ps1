<#
.SYNOPSIS
    Discord Classic Dark theme installer for TeamSpeak 6 (v2.0).

.DESCRIPTION
    Installs the dev.custom.discord theme extension into TeamSpeak 6 with all
    6 visual presets (72px full rail / minimalist rail / wide navigation, with
    and without channel banners) and optionally configures settings.db.

.PARAMETER Preset
    Preset selection:
      1 = Discord Dark (72px + bookmarks/chats, no banners)
      2 = Discord Dark + Banners (72px + bookmarks/chats + channel banners)
      3 = Discord Rail (minimalist 72px rail, no banners)
      4 = Discord Rail + Banners (Recommended: 72px rail + channel banners)
      5 = Discord Wide (wide left navigation, no banners)
      6 = Discord Wide + Banners (wide left navigation + channel banners)
      7 = Copy extension files only (keep current active theme)
      8 = Uninstall theme (remove extension and restore default TS6 style)

.PARAMETER ProfileName
    TeamSpeak profile folder name inside %APPDATA%\TeamSpeak (default: Default).

.PARAMETER SourceDir
    Local path to extension\ folder (auto-detected when run from cloned repo).

.PARAMETER RepoArchiveUrl
    GitHub repository branch ZIP archive URL used by remote irm | iex installs.

.PARAMETER AutoRestart
    Gracefully close TeamSpeak 6 (flushing SQLite WAL) and relaunch after setup.

.PARAMETER NoRestart
    Do not close or relaunch a running TeamSpeak 6 process.

.PARAMETER Uninstall
    Remove the installed extension and restore default TeamSpeak settings.

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

# GitHub repository used for remote installation (irm ... | iex):
$DefaultRepoSlug = "Roskud/teamspeak6-discord-theme"
$ExtId = "dev.custom.discord"

$Presets = [ordered]@{
    "1" = @{ Name = "Discord Dark";            File = "discord.css";              Tag = "Full 72px rail + bookmarks/chats (flat channels)" }
    "2" = @{ Name = "Discord Dark + Banners";  File = "discord-banners.css";      Tag = "Full 72px rail + bookmarks/chats + channel banners" }
    "3" = @{ Name = "Discord Rail";            File = "discord-rail.css";         Tag = "Minimalist 72px rail in calls (flat channels)" }
    "4" = @{ Name = "Discord Rail + Banners";  File = "discord-rail-banners.css"; Tag = "Recommended: minimalist 72px rail + channel banners" }
    "5" = @{ Name = "Discord Wide";            File = "discord-wide.css";         Tag = "Wide labeled sidebar (flat channels)" }
    "6" = @{ Name = "Discord Wide + Banners";  File = "discord-wide-banners.css"; Tag = "Wide labeled sidebar + channel banners" }
    "7" = @{ Name = "Install files only";      File = "";                         Tag = "Copy all 6 styles without modifying settings.db" }
    "8" = @{ Name = "Uninstall theme";         File = "";                         Tag = "Remove dev.custom.discord and restore default style" }
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
    try { Clear-Host } catch {}
    Write-Color "====================================================================`n" "Cyan"
    Write-Color "   Discord Classic Dark for TeamSpeak 6 - Theme Installer (v2.0)`n" "White"
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
            throw "TeamSpeak profile '$RequestedName' was not found under $(Join-Path $env:APPDATA 'TeamSpeak')."
        }
        return (Join-Path $env:APPDATA "TeamSpeak\Default")
    }

    if (-not [string]::IsNullOrWhiteSpace($RequestedName)) {
        $match = $Profiles | Where-Object { (Split-Path $_ -Leaf) -ieq $RequestedName } | Select-Object -First 1
        if (-not $match) {
            $avail = ($Profiles | ForEach-Object { Split-Path $_ -Leaf }) -join ", "
            throw "TeamSpeak profile '$RequestedName' was not found. Available profiles: $avail"
        }
        return $match
    }

    if ($Profiles.Count -eq 1) {
        return $Profiles[0]
    }

    $def = $Profiles | Where-Object { (Split-Path $_ -Leaf) -ieq "Default" } | Select-Object -First 1
    if ($AllowInteractive) {
        Write-Color "Multiple TeamSpeak profiles detected:`n" "White"
        for ($i = 0; $i -lt $Profiles.Count; $i++) {
            $leaf = Split-Path $Profiles[$i] -Leaf
            Write-Color ("  [{0}] " -f ($i + 1)) "Cyan" -NoNewline
            Write-Color "$leaf " "White" -NoNewline
            Write-Color "($($Profiles[$i]))`n" "DarkGray"
        }
        $ans = Read-Host "Select profile [1-$($Profiles.Count)] (Enter = 1)"
        if ([string]::IsNullOrWhiteSpace($ans)) {
            return $(if ($def) { $def } else { $Profiles[0] })
        }
        $idx = 0
        if ([int]::TryParse($ans.Trim(), [ref]$idx) -and $idx -ge 1 -and $idx -le $Profiles.Count) {
            return $Profiles[$idx - 1]
        }
        throw "Invalid profile selection: $ans"
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
    private static extern int sqlite3_open_v2(byte[] filename, out IntPtr ppDb, int flags, IntPtr zVfs);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_close_v2(IntPtr db);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    private static extern int sqlite3_exec(IntPtr db, byte[] sql, IntPtr cb, IntPtr arg, out IntPtr errMsg);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern void sqlite3_free(IntPtr ptr);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    private static extern int sqlite3_prepare_v2(IntPtr db, byte[] zSql, int nByte, out IntPtr ppStmt, out IntPtr pzTail);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_bind_text(IntPtr pStmt, int idx, byte[] val, int n, IntPtr freeFn);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_step(IntPtr pStmt);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_finalize(IntPtr pStmt);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_changes(IntPtr db);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern IntPtr sqlite3_column_text(IntPtr pStmt, int iCol);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern int sqlite3_column_bytes(IntPtr pStmt, int iCol);

    [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
    public static extern IntPtr sqlite3_errmsg(IntPtr db);

    private static byte[] ToUtf8Z(string s) {
        byte[] b = Encoding.UTF8.GetBytes(s);
        byte[] res = new byte[b.Length + 1];
        Buffer.BlockCopy(b, 0, res, 0, b.Length);
        return res;
    }

    private static string ReadUtf8Z(IntPtr ptr) {
        if (ptr == IntPtr.Zero) return null;
        int len = 0;
        while (Marshal.ReadByte(ptr, len) != 0) len++;
        if (len == 0) return "";
        byte[] buf = new byte[len];
        Marshal.Copy(ptr, buf, 0, len);
        return Encoding.UTF8.GetString(buf);
    }

    private static string GetError(IntPtr db) {
        if (db == IntPtr.Zero) return "unknown sqlite error";
        return ReadUtf8Z(sqlite3_errmsg(db)) ?? "sqlite error";
    }

    private static IntPtr OpenUtf8(string dbPath, int flags) {
        IntPtr db = IntPtr.Zero;
        int rc = sqlite3_open_v2(ToUtf8Z(dbPath), out db, flags, IntPtr.Zero);
        if (rc != 0) {
            string err = GetError(db);
            if (db != IntPtr.Zero) sqlite3_close_v2(db);
            throw new Exception("sqlite3_open_v2 failed (" + rc + "): " + err);
        }
        return db;
    }

    public static void CheckpointTruncate(string dbPath) {
        IntPtr db = IntPtr.Zero;
        try {
            db = OpenUtf8(dbPath, 2);
            IntPtr errPtr;
            int rc = sqlite3_exec(db, ToUtf8Z("PRAGMA busy_timeout=3000; PRAGMA wal_checkpoint(TRUNCATE);"), IntPtr.Zero, IntPtr.Zero, out errPtr);
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
            db = OpenUtf8(dbPath, 1);
            IntPtr tail;
            byte[] sql = ToUtf8Z("SELECT value FROM json_blobs WHERE key='general_settings' LIMIT 1;");
            int rc = sqlite3_prepare_v2(db, sql, -1, out stmt, out tail);
            if (rc != 0) throw new Exception("sqlite3_prepare_v2 failed (" + rc + "): " + GetError(db));
            rc = sqlite3_step(stmt);
            if (rc == 101) return null;
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
            db = OpenUtf8(dbPath, 2);
            IntPtr errPtr;
            int rcTimeout = sqlite3_exec(db, ToUtf8Z("PRAGMA busy_timeout=3000;"), IntPtr.Zero, IntPtr.Zero, out errPtr);
            if (errPtr != IntPtr.Zero) sqlite3_free(errPtr);
            if (rcTimeout != 0) throw new Exception("busy_timeout failed (" + rcTimeout + "): " + GetError(db));

            IntPtr tail;
            byte[] sql = ToUtf8Z("UPDATE json_blobs SET value = ?1, timestamp = COALESCE(timestamp + 1, 0) WHERE key = 'general_settings';");
            int rc = sqlite3_prepare_v2(db, sql, -1, out stmt, out tail);
            if (rc != 0) throw new Exception("sqlite3_prepare_v2 failed (" + rc + "): " + GetError(db));
            byte[] utf8 = Encoding.UTF8.GetBytes(jsonText);
            rc = sqlite3_bind_text(stmt, 1, utf8, utf8.Length, new IntPtr(-1));
            if (rc != 0) throw new Exception("sqlite3_bind_text failed (" + rc + "): " + GetError(db));
            rc = sqlite3_step(stmt);
            if (rc != 101) throw new Exception("sqlite3_step failed (" + rc + "): " + GetError(db));
            if (sqlite3_changes(db) < 1) throw new Exception("general_settings row not found in settings.db");
            int rcCkpt = sqlite3_exec(db, ToUtf8Z("PRAGMA wal_checkpoint(TRUNCATE);"), IntPtr.Zero, IntPtr.Zero, out errPtr);
            if (errPtr != IntPtr.Zero) sqlite3_free(errPtr);
            if (rcCkpt != 0) throw new Exception("wal_checkpoint failed (" + rcCkpt + "): " + GetError(db));
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
        if ($appearance.PSObject.Properties['show_servertree_channel_banners']) {
            $appearance.PSObject.Properties.Remove('show_servertree_channel_banners')
        }
        Set-JsonProp -Target $workflow -Name "keepActiveItemsInList" -Value $true
    } else {
        # Expose channel banner metadata so all 6 theme presets work without reinstalling
        Set-JsonProp -Target $appearance -Name "user_style" -Value $StyleName
        Set-JsonProp -Target $appearance -Name "show_servertree_channel_banners" -Value $true
        # Prevent active connected server from duplicating in Bookmarks while keeping other saved servers clickable
        Set-JsonProp -Target $workflow -Name "keepActiveItemsInList" -Value $false
    }

    $bakPath = "$SettingsDbPath.bak"
    if (-not (Test-Path $bakPath)) {
        Copy-Item -Path $SettingsDbPath -Destination $bakPath
    }

    $newJson = $obj | ConvertTo-Json -Depth 32 -Compress
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

    if (-not $ArchiveUrl) {
        if ($DefaultRepoSlug -match '<USER>|<REPO>') {
            throw "Local 'extension' folder not found and GitHub repository slug is not configured."
        }
        $ArchiveUrl = "https://github.com/$DefaultRepoSlug/archive/refs/heads/main.zip"
    }

    Write-Color "-> Downloading theme package from GitHub...`n" "Cyan"
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
        throw "Could not find extension/package.json inside downloaded archive."
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
    throw "Timed out waiting for TeamSpeak.exe to close cleanly."
}

function Invoke-InstallerMain {
    $activePreset = $Preset
    if ($Uninstall) {
        if ($Preset -ne 0 -and $Preset -ne 8) {
            Write-Color "[i] -Uninstall overrides -Preset $Preset.`n" "Yellow"
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
        Write-Color "TeamSpeak Profile: " "DarkGray" -NoNewline
        Write-Color "$targetProfile`n`n" "White"
        Write-Color "Choose a Discord Classic Dark preset:`n`n" "White"

        foreach ($k in $Presets.Keys) {
            $p = $Presets[$k]
            $numColor = if ($k -eq "4") { "Green" } elseif ($k -eq "8") { "Red" } else { "Cyan" }
            Write-Color ("  [{0}] " -f $k) $numColor -NoNewline
            Write-Color ("{0,-24}" -f $p.Name) "White" -NoNewline
            Write-Color " - $($p.Tag)`n" "DarkGray"
        }
        Write-Color "`n  [Q] " "DarkGray" -NoNewline
        Write-Color "Quit`n`n" "DarkGray"

        while ($true) {
            $choice = Read-Host "Enter option [1-8] (Enter = 4: Discord Rail + Banners)"
            if ([string]::IsNullOrWhiteSpace($choice)) {
                $activePreset = 4
                break
            }
            if ($choice.Trim().ToUpper() -eq "Q") {
                Write-Color "`nCancelled by user.`n" "Yellow"
                return
            }
            $parsed = 0
            if ([int]::TryParse($choice.Trim(), [ref]$parsed) -and $Presets.Contains("$parsed")) {
                $activePreset = $parsed
                break
            }
            Write-Color "Invalid selection. Enter a number between 1 and 8, or Q.`n" "Red"
        }
        Write-Host ""
    }

    $selected = $Presets["$activePreset"]
    Write-Color "Selected preset: " "White" -NoNewline
    Write-Color "$($selected.Name)`n" "Cyan"

    $tsExePath = Find-TeamSpeakExe
    $tempRoot = Join-Path $env:TEMP ("ts6-discord-install-" + [guid]::NewGuid().ToString("N"))

    try {
        $srcDir = $null
        if ($activePreset -ne 8) {
            $srcDir = Resolve-ExtensionSource -ExplicitSource $SourceDir -ArchiveUrl $RepoArchiveUrl -TempRoot $tempRoot
        }

        $tsRunning = @(Get-Process -Name "TeamSpeak" -ErrorAction SilentlyContinue)
        $shouldRestart = $false
        if ($tsRunning.Count -gt 0 -and -not $NoRestart) {
            if ($AutoRestart) {
                $shouldRestart = $true
            } elseif ($interactiveMode) {
                $ans = Read-Host "TeamSpeak 6 is currently running. Close cleanly, install, and restart? [Y/n]"
                if ([string]::IsNullOrWhiteSpace($ans) -or $ans.Trim().ToLower().StartsWith("y")) {
                    $shouldRestart = $true
                }
            }
        }

        if ($shouldRestart) {
            Write-Color "-> Closing TeamSpeak 6 cleanly...`n" "DarkGray"
            Stop-TeamSpeakSafely
        } elseif ($tsRunning.Count -gt 0 -and $activePreset -ne 7) {
            Write-Color "   [!] TeamSpeak 6 is still running - restart it manually (or pass -AutoRestart) after updating settings.db.`n" "Yellow"
        }

        if ($activePreset -eq 8) {
            if (Test-Path $extTargetDir) {
                Remove-Item -Path $extTargetDir -Recurse -Force
                Write-Color "[OK] Removed extension directory: $extTargetDir`n" "Green"
            } else {
                Write-Color "[i] Extension was not installed.`n" "Yellow"
            }
            if (Test-Path $settingsDb) {
                try {
                    if (Update-SettingsDb -SettingsDbPath $settingsDb -StyleName "") {
                        Write-Color "[OK] Restored default theme settings in settings.db`n" "Green"
                    }
                } catch {
                    Write-Color "   [!] Could not update settings.db automatically: $($_.Exception.Message)`n" "Yellow"
                }
            }
        } else {
            New-Item -ItemType Directory -Path (Split-Path $extTargetDir -Parent) -Force | Out-Null
            if (Test-Path $extTargetDir) {
                Remove-Item -Path $extTargetDir -Recurse -Force
            }
            Copy-Item -Path $srcDir -Destination $extTargetDir -Recurse -Force
            Write-Color "[OK] Installed all 6 theme presets to: $extTargetDir`n" "Green"

            if ($activePreset -ge 1 -and $activePreset -le 6) {
                $styleName = $selected.Name
                $styleId = "$ExtId//$styleName"
                $dbOk = $false
                try {
                    $dbOk = Update-SettingsDb -SettingsDbPath $settingsDb -StyleName $styleId
                } catch {
                    Write-Color "   [!] Could not update settings.db automatically: $($_.Exception.Message)`n" "Yellow"
                }
                if ($dbOk) {
                    Write-Color "[OK] Activated '$styleName' and configured banners/rail in settings.db (backup: settings.db.bak)`n" "Green"
                } else {
                    Write-Color "[i] Open TeamSpeak 6 -> Settings -> Appearance -> Theme and select '$styleName'`n" "Yellow"
                }
            }
        }

        if ($shouldRestart) {
            if ($tsExePath -and (Test-Path $tsExePath)) {
                Write-Color "-> Launching TeamSpeak 6...`n" "Cyan"
                Start-Process -FilePath $tsExePath
            } else {
                Write-Color "[i] TeamSpeak.exe not found - please launch TeamSpeak 6 manually.`n" "Yellow"
            }
        } elseif ($tsRunning.Count -eq 0 -and -not $NoRestart) {
            if ($tsExePath -and (Test-Path $tsExePath)) {
                $shouldLaunchNow = $false
                if ($AutoRestart) {
                    $shouldLaunchNow = $true
                } elseif ($interactiveMode) {
                    $launch = Read-Host "Launch TeamSpeak 6 now? [Y/n]"
                    if ([string]::IsNullOrWhiteSpace($launch) -or $launch.Trim().ToLower().StartsWith("y")) {
                        $shouldLaunchNow = $true
                    }
                }
                if ($shouldLaunchNow) {
                    Start-Process -FilePath $tsExePath
                }
            }
        }

        Write-Color "`nDone! " "Green"
        if ($activePreset -eq 8) {
            Write-Color "Discord Classic Dark theme has been uninstalled.`n" "Gray"
        } else {
            Write-Color "You can switch all 6 variants anytime in TeamSpeak 6: Settings -> Appearance -> Theme.`n" "Gray"
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
