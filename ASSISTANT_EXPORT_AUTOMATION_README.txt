============================================================
Liberty AI Trade — Assistant Export Automation System
============================================================

Purpose:
--------
Automatically export a safe project bundle for ChatGPT
whenever code changes are detected inside the project root.

This system runs quietly in the background and batches changes
(debounce) so exports happen only after real edits, not on every save.


Scripts Installed:
------------------
1) Export-OnChange-Watcher.ps1
   - Location: C:\Users\MMAPR\Liberty AI Trade\Export-OnChange-Watcher.ps1
   - Watches project changes and triggers exports

2) Export-Assistant-Bundle.ps1
   - Runs the safe export (env + secrets excluded)


Scheduled Task Installed:
-------------------------
Name:  Liberty AI – Assistant Export On Change
Trigger: Runs at every Windows logon
Mode: Hidden background PowerShell window
Priv: Highest


Log Locations:
--------------
General watcher log:
C:\Users\MMAPR\Liberty AI Trade\Frontend\logs\assistant_exports\export_watcher.log

Export ZIP output:
C:\Users\MMAPR\Liberty AI Trade\Frontend\logs\assistant_exports\assistant_export_*.zip


How To Stop the Automation
--------------------------
Run in PowerShell (Admin):

Unregister-ScheduledTask -TaskName "Liberty AI – Assistant Export On Change" -Confirm:$false


How To Start Again
------------------
Run (from root folder):

powershell -NoProfile -ExecutionPolicy Bypass -File .\Register-Assistant-Export-OnChange.ps1


How To Run Export Manually
--------------------------
powershell -NoProfile -ExecutionPolicy Bypass -File .\Export-Assistant-Bundle.ps1


Safety Notes:
-------------
✅ .env files excluded (not exported)
✅ ZIP archives stored locally only
✅ Debounce prevents excessive exports
✅ Logs kept for transparency
🚫 Does NOT upload to cloud (local only)
🚫 Does NOT transmit any filesystem contents unless you manually upload ZIP


Editing Watcher Settings (optional)
-----------------------------------
Debounce timing default = 60 seconds
Modify inside Export-OnChange-Watcher.ps1 if needed:

param([int]$DebounceSeconds = 60)


If Something Breaks
-------------------
To reset:
1) Stop task (see above)
2) Delete export logs if desired
3) Re-run Register-Assistant-Export-OnChange.ps1


Confirmation History:
---------------------
Last setup verified working: Yes
Mirroring removed: Yes
Tracking method: Local file watcher + scheduled task
============================================================
