#!/usr/bin/pwsh

Param([switch]$j, [string]$f)

$DEVICE = "COM3"
$Json = $false
$DEBUG = $false

Write-Host 'Checking for ampy in your command path:'
try {
  (Get-Command ampy).Path
} catch {
  Write-Host "Couldn't find ampy. Please make sure it's installed and in your path`n"
  Throw $_
}

if ($PSBoundParameters.ContainsKey('f')) {
  $DEVICE=$f
}
Write-Host "Using device $DEVICE. (Use -f to specify your port device)"
if ($PSBoundParameters.ContainsKey('j')) {
  $Json = $true
}

if ($Json) {
  Write-Host "Pushing tokens.js to $DEVICE"
  if ($DEBUG) { Write-Host "ampy --port $DEVICE put tokens.json" }
  ampy --port $DEVICE put tokens.json
} else {
  Write-Host "Skipped tokens.json. (Use -j to push tokens)"
}

Write-Host "About to copy python code to $DEVICE"
$files = 'blinkers.py', 'funcs.py', 'api.py', 'pixel.py', 'main.py', 'spectre.py'
foreach ($file in $files) {
  Write-Host "= pushing $file"
  if ($DEBUG) { Write-Host "ampy --port $DEVICE put $file" }
  ampy --port $DEVICE put $file
}
Write-Host "About to copy secrets.py; consult README if you haven't set this up yet."
if ($DEBUG) { Write-Host "ampy --port $DEVICE put secrets.py" }
ampy --port $DEVICE put secrets.py
