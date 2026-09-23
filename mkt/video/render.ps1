# supEars countdown video renderer
# Usage:
#   powershell -ExecutionPolicy Bypass -File mkt\video\render.ps1 -Days 17 -OutBase 008-seventeen-days-v8
# Renders BOTH landscape and vertical by default. Language list lives in langs.txt.
# The screen blend runs in RGB (gbrp) on purpose: blending in YUV shifts chroma
# and paints the whole frame magenta (that bug shipped in v7 - do not "simplify" back).

param(
  [int]$Days = 17,
  [string]$OutBase = "008-seventeen-days-v8",
  [string]$Music = "",
  [switch]$LandscapeOnly,
  [switch]$VerticalOnly
)

# ---------------- CONFIG (edit here) ----------------
$VideoDir  = $PSScriptRoot
$Repo      = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Logo      = Join-Path $Repo "mkt\assets\supEarsLogoV3.png"
$Emblem    = Join-Path $Repo "mkt\assets\supEarsEmblem.png"
$LangsFile = Join-Path $VideoDir "langs.txt"
if (-not $Music) { $Music = Join-Path $VideoDir "music_instant14.m4a" }
$FontDir   = "C:\Users\777\AppData\Local\Temp\opencode\fonts"

$DUR       = 14        # total seconds
$BRAND_END = 4         # brand screen: 0..4s
$END_START = 10        # end card: 10..14s
$BGLUR     = 8
$DARKEN    = -0.25
$ZOOM      = 0.10      # total push-in across the whole video
$FFADE     = 0.3       # element fade length
$FPS       = 24

$TAGLINE  = "The Ear that understands your language."
$DATE     = "October 10, 2026"
$DAYSWORD = "DAYS TO GO"
$DL       = "Download free"
$URL      = "github.com/humbleangel/supEars_Official"
# ----------------------------------------------------

function FF([string]$p) { ($p -replace '\\', '/') -replace ':', '\:' }
function N([double]$v) { $v.ToString('0.###', [System.Globalization.CultureInfo]::InvariantCulture) }
function DTEsc([string]$s) { $s -replace "'", "\'" }

$Fonts = @{
  main = FF "$env:WINDIR\Fonts\segoeui.ttf"
  bold = FF "$env:WINDIR\Fonts\segoeuib.ttf"
  sc   = FF "$FontDir\NotoSansSC.ttf"
  jp   = FF "$FontDir\NotoSansJP.ttf"
  kr   = FF "$env:WINDIR\Fonts\malgun.ttf"
  in   = FF "$FontDir\NotoSansDevanagari.ttf"
  th   = FF "$env:WINDIR\Fonts\LeelawUI.ttf"
  ar   = FF "$FontDir\NotoNaskhArabic.ttf"
}

$Langs = @()
Get-Content -Encoding UTF8 $LangsFile | Where-Object { $_.Trim() -ne "" } | ForEach-Object {
  $p = $_.Split("|")
  $key = $p[1].Trim()
  if (-not $Fonts.ContainsKey($key)) { throw "Unknown font key '$key' in langs.txt" }
  $Langs += @{ t = $p[0].Trim(); f = $key }
}
if ($Langs.Count -eq 0) { throw "langs.txt is empty" }

$TmpDir = Join-Path $VideoDir "tmp"
if (-not (Test-Path $TmpDir)) { New-Item -ItemType Directory -Path $TmpDir | Out-Null }
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
for ($i = 0; $i -lt $Langs.Count; $i++) {
  $tp = Join-Path $TmpDir ("lang_{0:d2}.txt" -f $i)
  [System.IO.File]::WriteAllText($tp, $Langs[$i].t, $utf8NoBom)
  $Langs[$i].tf = (FF $tp)
}

function DrawText([string]$font, [string]$text, [int]$size, [string]$x, [string]$y, [string]$enable, [string]$alpha, [string]$textFile = "") {
  if ($textFile) { $txtOpt = "textfile='$textFile'" } else { $txtOpt = "text='$(DTEsc $text)'" }
  $s = "drawtext=fontfile='${font}':${txtOpt}:fontcolor=white:fontsize=${size}:x=${x}:y=${y}:shadowcolor=black:shadowx=2:shadowy=2"
  if ($enable) { $s += ":enable='$enable'" }
  if ($alpha) { $s += ":alpha='$alpha'" }
  return $s
}

$FadeIn  = "if(lt(t\,0.3)\,t/0.3\,if(gt(t\,9.7)\,(10-t)/0.3\,1))"
$FadeEnd = "if(lt(t\,10.3)\,(t-10)/0.3\,if(gt(t\,13.7)\,(14-t)/0.3\,1))"

$Orientations = @(
  @{ Name = "land"; W = 1920; H = 1080; ZS = "3840:2160"; TagSplit = $false
     Em1Y = 150; Em2Y = 50;  Em1S = 200; Em2S = 240
     TagY = 500; LangY = 660; LangS = 84
     NumY = "(h/2-text_h)-170"; NumS = 190; WordY = "(h/2+10)"; WordS = 52
     DLY = "(h/2+80)"; DLS = 62; DateY = "(h/2+150)"; Dates = 62; UrlY = "(h/2+230)"; UrlS = 38 },
  @{ Name = "vertical"; W = 1080; H = 1920; ZS = "2160:3840"; TagSplit = $true
     Em1Y = 520; Em2Y = 300; Em1S = 180; Em2S = 220
     TagY = 880; LangY = 1090; LangS = 76
     NumY = "560"; NumS = 200; WordY = "1010"; WordS = 50
     DLY = "1100"; DLS = 58; DateY = "1190"; Dates = 58; UrlY = "1300"; UrlS = 34 }
)

foreach ($o in $Orientations) {
  if ($LandscapeOnly -and $o.Name -ne "land") { continue }
  if ($VerticalOnly -and $o.Name -ne "vertical") { continue }

  # language flash filters, one slot each
  $n = $Langs.Count
  $slot = ($END_START - $BRAND_END) / $n
  $langDt = @()
  for ($i = 0; $i -lt $n; $i++) {
    $s = $BRAND_END + $i * $slot
    $e = $s + $slot
    $a = "if(lt(t\,$(N ($s + 0.05)))\,(t-$(N $s))/0.05\,if(gt(t\,$(N ($e - 0.05)))\,($(N $e)-t)/0.05\,1))"
    $langDt += DrawText $Fonts[$Langs[$i].f] "" $o.LangS "(w-text_w)/2" $o.LangY "between(t,$(N $s),$(N $e))" $a $Langs[$i].tf
  }

  $dt = @()
  if ($o.TagSplit) {
    $dt += DrawText $Fonts.main "The Ear that understands" 54 "(w-text_w)/2" $o.TagY "between(t,0,10)" $FadeIn
    $dt += DrawText $Fonts.main "your language." 54 "(w-text_w)/2" ($o.TagY + 80) "between(t,0,10)" $FadeIn
  } else {
    $dt += DrawText $Fonts.main $TAGLINE 60 "(w-text_w)/2" $o.TagY "between(t,0,10)" $FadeIn
  }
  $dt += $langDt
  $dt += DrawText $Fonts.bold "$Days" $o.NumS "(w-text_w)/2" $o.NumY "between(t,10,14)" $FadeEnd
  $dt += DrawText $Fonts.main $DAYSWORD $o.WordS "(w-text_w)/2" $o.WordY "between(t,10,14)" $FadeEnd
  $dt += DrawText $Fonts.bold $DL $o.DLS "(w-text_w)/2" $o.DLY "between(t,10,14)" $FadeEnd
  $dt += DrawText $Fonts.bold $DATE $o.Dates "(w-text_w)/2" $o.DateY "between(t,10,14)" $FadeEnd
  $dt += DrawText $Fonts.main $URL $o.UrlS "(w-text_w)/2" $o.UrlY "between(t,10,14)" $FadeEnd

  # video chain: emblems overlay a black canvas (alpha-safe), THEN screen in gbrp (RGB)
  $fc = "[1]scale=$($o.Em1S):-1,fade=t=in:st=0:d=0.3,fade=t=out:st=3.7:d=0.3[em1];" +
        "[1]scale=$($o.Em2S):-1,fade=t=in:st=10:d=0.3,fade=t=out:st=13.7:d=0.3[em2];" +
        "[2]format=gbrp[cv];" +
        "[cv][em1]overlay=(W-w)/2:$($o.Em1Y):enable='between(t,0,4)'[c1];" +
        "[c1][em2]overlay=(W-w)/2:$($o.Em2Y):enable='between(t,10,14)'[c2];" +
        "[0]scale=$($o.W):$($o.H):force_original_aspect_ratio=increase,crop=$($o.W):$($o.H),gblur=sigma=$BGLUR,eq=brightness=$DARKEN,format=gbrp[bg];" +
        "[bg][c2]blend=all_mode=screen,format=yuv420p[scr];" +
        "[scr]" + ($dt -join ",") + ",scale=$($o.ZS),zoompan=z='1+$ZOOM*on/335':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=$($o.W)x$($o.H):fps=$FPS,fade=t=in:st=0:d=0.3,fade=t=out:st=13.7:d=0.3[v]"

  if ($o.Name -eq "vertical") { $outPath = Join-Path $VideoDir "$OutBase-vertical.mp4" }
  else { $outPath = Join-Path $VideoDir "$OutBase.mp4" }

  Write-Output "Rendering $outPath ..."
  Set-Content -Path (Join-Path $TmpDir "$($o.Name)_filter.txt") -Value $fc -Encoding UTF8
  & ffmpeg -y -v error `
    -loop 1 -framerate $FPS -t $DUR -i $Logo `
    -loop 1 -framerate $FPS -t $DUR -i $Emblem `
    -f lavfi -t $DUR -i "color=black:s=$($o.W)x$($o.H):r=$FPS" `
    -i $Music `
    -filter_complex $fc -map "[v]" -map 3:a `
    -c:v libx264 -pix_fmt yuv420p -r $FPS -c:a copy -shortest -t $DUR `
    $outPath
  if ($LASTEXITCODE -ne 0) { throw "ffmpeg failed for $outPath" }
  Write-Output "Done: $outPath"
}
