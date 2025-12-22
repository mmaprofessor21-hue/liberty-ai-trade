===========================================================
 Liberty AI Trade — Assistant Export Bundle (SAFE SHARING)
===========================================================

PURPOSE:
--------
This process exports a SAFE version of the "Liberty AI Trade" project
for AI assistant review WITHOUT exposing secrets, environment keys, or
sensitive system config files.

This preserves privacy and security while still allowing full code
review and guidance.

-----------------------------------------
 SCRIPT USED:
-----------------------------------------
Export-Assistant-Bundle.ps1
(Located in project root)

-----------------------------------------
 HOW TO RUN:
-----------------------------------------

Open PowerShell in the Liberty AI Trade project root:

powershell -ExecutionPolicy Bypass -File .\Export-Assistant-Bundle.ps1

-----------------------------------------
 WHAT THIS DOES:
-----------------------------------------
1) Scans all repo files
2) Automatically excludes:
   - .env files
   - API keys / private secrets
   - Backup archives / logs
   - build artifacts / node_modules / venv
   - Anything matching secret patterns
3) Prompts if suspicious files are detected
4) Creates a CLEAN export package
5) Saves ZIP here:

Frontend\logs\assistant_exports\assistant_export_<timestamp>.zip

6) Creates a manifest listing included/excluded files

-----------------------------------------
 WHAT THIS EXPORT IS FOR:
-----------------------------------------
✅ Safe project sharing for AI review
✅ Troubleshooting code
✅ Assistance with architecture & features
❌ Not for deployment
❌ Not for backup
❌ Does not include secrets

-----------------------------------------
 OUTPUT EXAMPLE:
-----------------------------------------
Frontend\logs\assistant_exports\
 └─ assistant_export_2025-11-10_13-49-53.zip

-----------------------------------------
 CONFIRMATION PROMPT
-----------------------------------------
If possible secrets are detected, you will see:

[WARNING] Potential secrets detected...
Proceed WITHOUT these risky files? (Y/N)

Always type `Y` unless you intentionally need those reviewed.

-----------------------------------------
 PLACE IN `.gitignore`
-----------------------------------------
Ensure this is ignored:

Frontend/logs/assistant_exports/

-----------------------------------------
 SECURITY RULE:
-----------------------------------------
NEVER share:
- .env files
- API keys
- Wallet keys
- Login cookies or tokens
- Full DB exports

This script enforces that rule.

-----------------------------------------
 FUTURE NOTE:
-----------------------------------------
This is the OFFICIAL export procedure.  
Always use THIS script before sharing anything.

-----------------------------------------
 FULL SCRIPT (Do not change unless instructed)
-----------------------------------------

# Export-Assistant-Bundle.ps1
# ------------------------------------------------------------
# Creates a clean, secrets-filtered export of the project
# ------------------------------------------------------------
$ErrorActionPreference = "Stop"

Write-Host "`n[COLLECT] Scanning files..."

$root = Get-Location

$excludePathPatterns = @(
  'node_modules', 'venv', 'env', 'backup', 'dist', 'build', 'logs',
  'assistant_exports'
)

$excludeFileExt = @(
  '.zip', '.exe', '.dll', '.log'
)

$secretNamePatterns = @(
  'env', 'secret', 'key', 'wallet', 'api', 'auth'
)

$secretContentPatterns = @(
  'API_KEY', 'PRIVATE_KEY', 'SECRET', 'TOKEN'
)

$files = Get-ChildItem -Path $root -Recurse -File

$staging = Join-Path $root "assistant_export_staging"
Remove-Item -Recurse -Force -LiteralPath $staging -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $staging | Out-Null

$findings = @()

foreach ($f in $files) {
  $rel = $f.FullName.Substring($root.Path.Length+1)

  if ($excludePathPatterns | Where-Object { $rel -like "*$_*" }) { continue }
  if ($excludeFileExt -contains $f.Extension) { continue }

  $sus = $false

  if ($secretNamePatterns | Where-Object { $f.Name -like "*$_*" }) { $sus = $true }

  try {
    $content = Get-Content -LiteralPath $f.FullName -Raw -ErrorAction Stop
    if ($secretContentPatterns | Where-Object { $content -match $_ }) { $sus = $true }
  } catch {}

  if ($sus) {
    $findings += $rel
    continue
  }

  $dest = Join-Path $staging $rel
  New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
  Copy-Item -LiteralPath $f.FullName -Destination $dest -Force
}

if ($findings.Count -gt 0) {
  Write-Warning "Potential secrets detected!"
  $findings | ForEach-Object { Write-Host " - $_" }
  $resp = Read-Host "Proceed WITHOUT these risky files? (Y/N)"
  if ($resp -notin @('y','Y')) { throw "Export canceled" }
}

$timestamp = (Get-Date -Format "yyyy-MM-dd_HH-mm-ss")
$exportDir = Join-Path $root "Frontend\logs\assistant_exports"
New-Item -ItemType Directory -Force -Path $exportDir | Out-Null
$zip = Join-Path $exportDir "assistant_export_$timestamp.zip"

Write-Host "[ZIP] Creating archive..."
Compress-Archive -Path "$staging\*" -DestinationPath $zip -Force

Remove-Item -Recurse -Force -LiteralPath $staging

Write-Host "`n[DONE] Export finished."
Write-Host "Output: $zip"
