param(
  [string]$OutDir = "$env:TEMP\opencode\supears_caps",
  [int]$AppPid = 0
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing, System.Windows.Forms

$proc = if ($AppPid -gt 0) { Get-Process -Id $AppPid -ErrorAction SilentlyContinue }
        else { Get-Process | Where-Object { $_.ProcessName -like "supEars*" } | Select-Object -First 1 }
if (-not $proc) { throw "supEars is not running" }

$code = @"
using System;
using System.Runtime.InteropServices;
public class Win {
  public delegate bool EnumWindowsProc(IntPtr h, IntPtr l);
  [StructLayout(LayoutKind.Sequential)] public struct R { public int L, T, Right, Bottom; }
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc cb, IntPtr l);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out R r);
  [DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr h, int cmd);
}
"@
Add-Type -TypeDefinition $code

$others = New-Object System.Collections.ArrayList
$cb = [Win+EnumWindowsProc]{
  param($h, $l)
  $pid2 = 0
  [Win]::GetWindowThreadProcessId($h, [ref]$pid2) | Out-Null
  if ([Win]::IsWindowVisible($h) -and -not [Win]::IsIconic($h)) {
    $r = New-Object Win+R
    [Win]::GetWindowRect($h, [ref]$r) | Out-Null
    $area = ($r.Right - $r.Left) * ($r.Bottom - $r.Top)
    $isEar = ($pid2 -eq $proc.Id -and $area -le 10000)
    if (-not $isEar) { [void]$others.Add($h) }
  }
  return $true
}
[Win]::EnumWindows($cb, [IntPtr]::Zero) | Out-Null

foreach ($h in $others) { [Win]::ShowWindowAsync($h, 6) | Out-Null }
Start-Sleep -Milliseconds 1800

$b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($b.Location, [System.Drawing.Point]::Empty, $b.Size)
$full = Join-Path $OutDir "desktop.png"
$bmp.Save($full, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()

foreach ($h in $others) { [Win]::ShowWindowAsync($h, 9) | Out-Null }

$img = [System.Drawing.Bitmap]::FromFile($full)
$minX = $img.Width; $minY = $img.Height; $maxX = -1; $maxY = -1
for ($y = 0; $y -lt [int]($img.Height * 0.45); $y++) {
  for ($x = [int]($img.Width * 0.55); $x -lt $img.Width; $x++) {
    $c = $img.GetPixel($x, $y)
    if ($c.G -gt 150 -and $c.B -gt 110 -and $c.R -lt 130) {
      if ($x -lt $minX) { $minX = $x }; if ($x -gt $maxX) { $maxX = $x }
      if ($y -lt $minY) { $minY = $y }; if ($y -gt $maxY) { $maxY = $y }
    }
  }
}
if ($maxX -lt 0) { $img.Dispose(); throw "no cyan ring found - ear not on screen?" }

$pad = 14
$minX = [Math]::Max(0, $minX - $pad); $minY = [Math]::Max(0, $minY - $pad)
$maxX = [Math]::Min($img.Width - 1, $maxX + $pad); $maxY = [Math]::Min($img.Height - 1, $maxY + $pad)
$rect = New-Object System.Drawing.Rectangle $minX, $minY, ($maxX - $minX + 1), ($maxY - $minY + 1)
$crop = $img.Clone($rect, $img.PixelFormat)
$ear = Join-Path $OutDir "ear.png"
$crop.Save($ear, [System.Drawing.Imaging.ImageFormat]::Png)
$crop.Dispose(); $img.Dispose()
"ear crop: $rect  -> $ear"
"minimized+restored windows: $($others.Count)"
