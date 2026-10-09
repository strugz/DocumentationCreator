<#
.SYNOPSIS
  Render every slide of a .pptx to PNG with PowerPoint, so each slide can be checked
  before the deck is reported (rules/60-proposal-slides.md section 6).

.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File tools/pptx_to_png.ps1 `
    -Path output/mode-b/my-app/export/My-App-Project-Proposal-Slides.pptx

.NOTES
  Needs Microsoft PowerPoint (Windows). Without it, use the pptx skill's LibreOffice
  conversion. Images go to <deck folder>/slides/ unless -OutDir is given.
#>
param(
  [Parameter(Mandatory = $true)][string]$Path,
  [string]$OutDir = "",
  [int]$Width = 1600,
  [int]$Height = 900
)
$ErrorActionPreference = "Stop"
$deck = (Resolve-Path $Path).Path
if (-not $OutDir) { $OutDir = Join-Path (Split-Path $deck) "slides" }
New-Item -ItemType Directory -Force $OutDir | Out-Null
$OutDir = (Resolve-Path $OutDir).Path

$app = New-Object -ComObject PowerPoint.Application
try {
  # ReadOnly, Untitled, WithWindow = false: nothing is shown or saved.
  $pres = $app.Presentations.Open($deck, $true, $false, $false)
  try {
    for ($i = 1; $i -le $pres.Slides.Count; $i++) {
      $file = Join-Path $OutDir ("slide-{0:D2}.png" -f $i)
      $pres.Slides.Item($i).Export($file, "PNG", $Width, $Height)
      Write-Output $file
    }
  } finally {
    $pres.Close()
  }
} finally {
  $app.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
