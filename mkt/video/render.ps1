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
if (-not $Music) { $Music = Join-Path $VideoDir "music_instant40.m4a" }
$FontDir   = "C:\Users\777\AppData\Local\Temp\opencode\fonts"

$DUR       = 40        # total seconds
$BRAND_END = 4         # languages start
$LANG_END  = 35        # languages end / end card starts
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
  if ($p.Count -lt 3) { throw "langs.txt lines need native|font|english" }
  $key = $p[1].Trim()
  if (-not $Fonts.ContainsKey($key)) { throw "Unknown font key '$key' in langs.txt" }
  $Langs += @{ t = $p[0].Trim(); f = $key; e = $p[2].Trim() }
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

$FadeIn  = "if(lt(t\,0.3)\,t/0.3\,if(gt(t\,34.7)\,(35-t)/0.3\,1))"
$FadeEnd = "if(lt(t\,35.3)\,(t-35)/0.3\,if(gt(t\,39.7)\,(40-t)/0.3\,1))"

$Orientations = @(
  @{ Name = "land"; W = 1920; H = 1080; ZS = "3840:2160"; TagSplit = $false
     EmY = 142; EmS = 260
     TagY = 500; LangY = 660; LangS = 84; Lang2Y = 760; Lang2S = 44
     NumY = 430; NumS = 190; WordY = 640; WordS = 52
     DLY = 720; DLS = 62; DateY = 790; Dates = 62; UrlY = 870; UrlS = 38 },
  @{ Name = "vertical"; W = 1080; H = 1920; ZS = "2160:3840"; TagSplit = $true
     EmY = 574; EmS = 240
     TagY = 880; LangY = 1090; LangS = 76; Lang2Y = 1180; Lang2S = 40
     NumY = 845; NumS = 200; WordY = 1065; WordS = 50
     DLY = 1145; DLS = 58; DateY = 1225; Dates = 58; UrlY = 1305; UrlS = 34 }
)

foreach ($o in $Orientations) {
  if ($LandscapeOnly -and $o.Name -ne "land") { continue }
  if ($VerticalOnly -and $o.Name -ne "vertical") { continue }

  # language flash filters, one slot each
  $n = $Langs.Count
  $slot = ($LANG_END - $BRAND_END) / $n
  $langDt = @()
  for ($i = 0; $i -lt $n; $i++) {
    $s = $BRAND_END + $i * $slot
    $e = $s + $slot
    $a = "if(lt(t\,$(N ($s + 0.05)))\,(t-$(N $s))/0.05\,if(gt(t\,$(N ($e - 0.05)))\,($(N $e)-t)/0.05\,1))"
    $langDt += DrawText $Fonts[$Langs[$i].f] "" $o.LangS "(w-text_w)/2" $o.LangY "between(t,$(N $s),$(N $e))" $a $Langs[$i].tf
    $langDt += DrawText $Fonts.main "($($Langs[$i].e))" $o.Lang2S "(w-text_w)/2" $o.Lang2Y "between(t,$(N $s),$(N $e))" $a
  }

  $dt = @()
  if ($o.TagSplit) {
    $dt += DrawText $Fonts.main "The Ear that understands" 54 "(w-text_w)/2" $o.TagY "between(t,0,35)" $FadeIn
    $dt += DrawText $Fonts.main "your language." 54 "(w-text_w)/2" ($o.TagY + 80) "between(t,0,35)" $FadeIn
  } else {
    $dt += DrawText $Fonts.main $TAGLINE 60 "(w-text_w)/2" $o.TagY "between(t,0,35)" $FadeIn
  }
  $dt += $langDt
  $dt += DrawText $Fonts.bold "$Days" $o.NumS "(w-text_w)/2" $o.NumY "between(t,35,40)" $FadeEnd
  $dt += DrawText $Fonts.main $DAYSWORD $o.WordS "(w-text_w)/2" $o.WordY "between(t,35,40)" $FadeEnd
  $dt += DrawText $Fonts.bold $DL $o.DLS "(w-text_w)/2" $o.DLY "between(t,35,40)" $FadeEnd
  $dt += DrawText $Fonts.bold $DATE $o.Dates "(w-text_w)/2" $o.DateY "between(t,35,40)" $FadeEnd
  $dt += DrawText $Fonts.main $URL $o.UrlS "(w-text_w)/2" $o.UrlY "between(t,35,40)" $FadeEnd

  # video chain: emblems overlay a black canvas (alpha-safe), THEN screen in gbrp (RGB)
  $fc = "[1]scale=$($o.EmS):-1,fade=t=in:st=0:d=0.3,fade=t=out:st=39.7:d=0.3[em];" +
        "[2]format=gbrp[cv];" +
        "[cv][em]overlay=(W-w)/2:$($o.EmY)[c1];" +
        "[0]scale=$($o.W):$($o.H):force_original_aspect_ratio=increase,crop=$($o.W):$($o.H),gblur=sigma=$BGLUR,eq=brightness=$DARKEN,format=gbrp[bg];" +
        "[bg][c1]blend=all_mode=screen,format=yuv420p[scr];" +
        "[scr]" + ($dt -join ",") + ",scale=$($o.ZS),zoompan=z='1+$ZOOM*on/959':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=$($o.W)x$($o.H):fps=$FPS,fade=t=in:st=0:d=0.3,fade=t=out:st=39.7:d=0.3[v]"

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
