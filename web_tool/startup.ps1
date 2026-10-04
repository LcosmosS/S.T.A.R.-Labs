$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
try {
  $starmapProbe = Invoke-WebRequest -Uri 'http://127.0.0.1:8080/' -TimeoutSec 2
  if ($starmapProbe.StatusCode -eq 200) { exit 0 }
} catch { }
$starmapNpm = (Get-Command npm.cmd).Source
Start-Process -FilePath $starmapNpm -ArgumentList @('run', 'dev') -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $PSScriptRoot 'app-startup.log') -RedirectStandardError (Join-Path $PSScriptRoot 'app-startup-error.log')
