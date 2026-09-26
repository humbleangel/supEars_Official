param(
  [string]$OutDir = "$env:TEMP\opencode\supears_caps",
  [string]$Exe = "D:\WORK_B\PRJS\supEars\supEars-0.9.36.exe"
)

$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$proc = Get-Process supEars -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $proc) { $proc = Start-Process -FilePath $Exe -PassThru; Start-Sleep -Seconds 7 }

$code = @"
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
public class Cap {
  public delegate bool EnumWindowsProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc cb, IntPtr l);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, System.Text.StringBuilder s, int n);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }

  public static string Grab(IntPtr h, string path) {
    RECT r; if (!GetWindowRect(h, out r)) return null;
    int w = r.Right - r.Left, ht = r.Bottom - r.Top;
    if (w < 40 || ht < 40) return null;
    using (Bitmap bmp = new Bitmap(w, ht, PixelFormat.Format32bppArgb))
    using (Graphics g = Graphics.FromImage(bmp)) {
      IntPtr hdc = g.GetHdc();
      bool ok = PrintWindow(h, hdc, 2);
      g.ReleaseHdc(hdc);
      if (!ok) return null;
      bmp.Save(path, ImageFormat.Png);
    }
    return w + "x" + ht;
  }
}
"@
Add-Type -TypeDefinition $code -ReferencedAssemblies "System.Drawing"

$found = New-Object System.Collections.ArrayList
$cb = [Cap+EnumWindowsProc]{
  param($h, $l)
  $pid2 = 0
  [Cap]::GetWindowThreadProcessId($h, [ref]$pid2) | Out-Null
  if ($pid2 -eq $proc.Id -and [Cap]::IsWindowVisible($h)) {
    $sb = New-Object System.Text.StringBuilder 256
    [Cap]::GetWindowText($h, $sb, 256) | Out-Null
    [void]$found.Add(@{ H = $h; Title = $sb.ToString() })
  }
  return $true
}
[Cap]::EnumWindows($cb, [IntPtr]::Zero) | Out-Null

$i = 0
foreach ($w in $found) {
  $i++
  $path = Join-Path $OutDir ("cap{0}.png" -f $i)
  $size = [Cap]::Grab($w.H, $path)
  "{0}  title='{1}'  rect={2}" -f (Split-Path $path -Leaf), $w.Title, $size
}
"pid: $($proc.Id)"
