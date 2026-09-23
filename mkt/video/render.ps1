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
$StopsFile = Join-Path $VideoDir "stops.txt"
if (-not $Music) { $Music = Join-Path $VideoDir "music_instant40.m4a" }
$FontDir   = "C:\Users\777\AppData\Local\Temp\opencode\fonts"

$DUR       = 40        # total seconds
$BRAND_END = 4         # languages start
$LANG_END  = 35        # languages end / end card starts
$BGLUR     = 8
$DARKEN    = -0.25
$ZOOM      = 0.10      # total push-in across the whole video
$FFADE     = 0.3       # element fade length
$FPS       = 12        # output framerate (owner: film look)

$TAGLINE  = "The Ear that understands your language."
$DATE     = "Launch: October 10, 2026"
$DAYSWORD = "DAYS TO GO"
$DL       = "Download for Free Now."
$JOIN     = "Join the Beta Group."
$URL      = "github.com/humbleangel/supEars_Official"

# flags under each language (flagcdn.com PNGs, public domain; keyed by langs.txt english column)
$FlagDir = Join-Path $VideoDir "flags"
$FlagMap = @{
  "English"              = "gb,us"
  "Portuguese"           = "br,pt"
  "Chinese"              = "cn"
  "Spanish"              = "es,mx"
  "French"               = "fr"
  "Japanese"             = "jp"
  "German"               = "de"
  "Korean"               = "kr"
  "Italian"              = "it"
  "Hindi"                = "in"
  "Russian"              = "ru"
  "Thai"                 = "th"
  "Ukrainian"            = "ua"
  "Arabic"               = "sa,eg"
  "Dutch"                = "nl"
  "Urdu"                 = "pk"
  "Polish"               = "pl"
  "Turkish"              = "tr"
  "Czech"                = "cz"
  "Hungarian"            = "hu"
  "Greek"                = "gr"
  "Romanian"             = "ro"
  "Swedish"              = "se"
  "Indonesian"           = "id"
  "Vietnamese"           = "vn"
}
# ----------------------------------------------------

function FF([string]$p) { ($p -replace '\\', '/') -replace ':', '\:' }
function N([double]$v) { $v.ToString('0.###', [System.Globalization.CultureInfo]::InvariantCulture) }
function DTEsc([string]$s) { ($s -replace "'", "\'") -replace ":", "\:" }

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
$StopMap = @{}
if (Test-Path $StopsFile) {
  Get-Content -Encoding UTF8 $StopsFile | Where-Object { $_.Trim() -ne "" } | ForEach-Object {
    $p = $_.Split("|")
    if ($p.Count -ge 2) { $StopMap[$p[0].Trim()] = $p[1].Trim() }
  }
}
for ($i = 0; $i -lt $Langs.Count; $i++) {
  $tp = Join-Path $TmpDir ("lang_{0:d2}.txt" -f $i)
  [System.IO.File]::WriteAllText($tp, $Langs[$i].t, $utf8NoBom)
  $Langs[$i].tf = (FF $tp)
  $Langs[$i].sf = $null
  if ($StopMap.ContainsKey($Langs[$i].e)) {
    $sp = Join-Path $TmpDir ("stop_{0:d2}.txt" -f $i)
    [System.IO.File]::WriteAllText($sp, $StopMap[$Langs[$i].e], $utf8NoBom)
    $Langs[$i].sf = (FF $sp)
  }
}

# build one flag strip per language (flagcdn PNGs, pre-composited with a dark gap)
$FlagOutDir = Join-Path $FlagDir "out"
if (-not (Test-Path $FlagOutDir)) { New-Item -ItemType Directory -Path $FlagOutDir | Out-Null }
$fi = 4   # ffmpeg input index (0 logo, 1 emblem, 2 canvas, 3 music)
for ($i = 0; $i -lt $Langs.Count; $i++) {
  $Langs[$i].fp = $null
  if (-not $FlagMap.ContainsKey($Langs[$i].e)) { Write-Output "WARN: no flag mapping for '$($Langs[$i].e)'"; continue }
  $src = @()
  foreach ($c in $FlagMap[$Langs[$i].e].Split(",")) {
    $p = Join-Path $FlagDir "$c.png"
    if (Test-Path $p) { $src += $p } else { Write-Output "WARN: missing flag file $c.png" }
  }
  if ($src.Count -eq 0) { continue }
  $outPng = Join-Path $FlagOutDir ("lang_{0:d2}.png" -f $i)
  if ($src.Count -eq 1) {
    & ffmpeg -y -v error -i $src[0] -vf "scale=-1:160" $outPng
  } else {
    & ffmpeg -y -v error -i $src[0] -i $src[1] -filter_complex "[0]scale=-1:160[a];[1]scale=-1:160[b];[a]pad=iw+16:ih:0:0:black[ap];[ap][b]hstack=inputs=2" $outPng
  }
  if ($LASTEXITCODE -ne 0) { throw "flag strip failed for $($Langs[$i].e)" }
  $Langs[$i].fp = $outPng
  $Langs[$i].fi = $fi
  $fi++
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
  @{ Name = "land"; W = 1920; H = 1080; ZS = "3840:2160"; TagSplit = $false; Zoom = 0.10
     EmY = 142; EmS = 260
     TagY = 500; LangY = 660; LangS = 84; Lang2Y = 760; Lang2S = 44
     FlagH = 54; FlagY = 830; StopY = 905; StopS = 40
     SupY = 400; SupS = 70
     NumY = 490; NumS = 190; WordY = 720; WordS = 52
     DLY = 790; DLS = 62; JoinY = 870; DateY = 950; Dates = 62; UrlY = 1025; UrlS = 38 },
  @{ Name = "vertical"; W = 1080; H = 1920; ZS = "2160:3840"; TagSplit = $true; Zoom = 0.20
     EmY = 574; EmS = 240
     TagY = 880; LangY = 1090; LangS = 76; Lang2Y = 1180; Lang2S = 40
     FlagH = 48; FlagY = 1245; StopY = 1320; StopS = 36
     SupY = 820; SupS = 64
     NumY = 905; NumS = 200; WordY = 1150; WordS = 50
     DLY = 1220; DLS = 58; JoinY = 1298; DateY = 1376; Dates = 58; UrlY = 1455; UrlS = 34 }
)

foreach ($o in $Orientations) {
  if ($LandscapeOnly -and $o.Name -ne "land") { continue }
  if ($VerticalOnly -and $o.Name -ne "vertical") { continue }

  # language flash filters, one slot each
  $n = $Langs.Count
  $slot = ($LANG_END - $BRAND_END) / $n
  $langDt = @()
  $slots = @()
  for ($i = 0; $i -lt $n; $i++) {
    $s = $BRAND_END + $i * $slot
    $e = $s + $slot
    $slots += , @($s, $e)
    $a = "if(lt(t\,$(N ($s + 0.1)))\,(t-$(N $s))/0.1\,if(gt(t\,$(N ($e - 0.1)))\,($(N $e)-t)/0.1\,1))"
    $langDt += DrawText $Fonts[$Langs[$i].f] "" $o.LangS "(w-text_w)/2" $o.LangY "between(t,$(N $s),$(N $e))" $a $Langs[$i].tf
    $langDt += DrawText $Fonts.main "($($Langs[$i].e))" $o.Lang2S "(w-text_w)/2" $o.Lang2Y "between(t,$(N $s),$(N $e))" $a
    if ($Langs[$i].sf) {
      $langDt += DrawText $Fonts[$Langs[$i].f] "" $o.StopS "(w-text_w)/2" $o.StopY "between(t,$(N $s),$(N $e))" $a $Langs[$i].sf
    }
  }

  # flag overlays under the language name, same slot window
  $flagChain = ""
  $prev = "scr"
  for ($i = 0; $i -lt $n; $i++) {
    if (-not $Langs[$i].fp) { continue }
    $s = $slots[$i][0]; $e = $slots[$i][1]
    $flagChain += "[$($Langs[$i].fi)]scale=-1:$($o.FlagH),format=rgba,fade=t=in:st=$(N $s):d=0.2:alpha=1,fade=t=out:st=$(N ($e - 0.2)):d=0.2:alpha=1[fl$i];[$prev][fl$i]overlay=(W-w)/2:$($o.FlagY):enable='between(t,$(N $s),$(N $e))'[fo$i];"
    $prev = "fo$i"
  }

  $dt = @()
  if ($o.TagSplit) {
    $dt += DrawText $Fonts.main "The Ear that understands" 54 "(w-text_w)/2" $o.TagY "between(t,0,35)" $FadeIn
    $dt += DrawText $Fonts.main "your language." 54 "(w-text_w)/2" ($o.TagY + 80) "between(t,0,35)" $FadeIn
  } else {
    $dt += DrawText $Fonts.main $TAGLINE 60 "(w-text_w)/2" $o.TagY "between(t,0,35)" $FadeIn
  }
  $dt += $langDt
  $dt += DrawText $Fonts.bold "supEars" $o.SupS "(w-text_w)/2" $o.SupY "between(t,35,40)" $FadeEnd
  $dt += DrawText $Fonts.bold "$Days" $o.NumS "(w-text_w)/2" $o.NumY "between(t,35,40)" $FadeEnd
  $dt += DrawText $Fonts.main $DAYSWORD $o.WordS "(w-text_w)/2" $o.WordY "between(t,35,40)" $FadeEnd
  $dt += DrawText $Fonts.bold $DL $o.DLS "(w-text_w)/2" $o.DLY "between(t,35,40)" $FadeEnd
  $dt += DrawText $Fonts.main $JOIN $o.DLS "(w-text_w)/2" $o.JoinY "between(t,35,40)" $FadeEnd
  $dt += DrawText $Fonts.bold $DATE $o.Dates "(w-text_w)/2" $o.DateY "between(t,35,40)" $FadeEnd
  $dt += DrawText $Fonts.main $URL $o.UrlS "(w-text_w)/2" $o.UrlY "between(t,35,40)" $FadeEnd

  # video chain: emblems overlay a black canvas (alpha-safe), THEN screen in gbrp (RGB)
  $fc = "[1]scale=$($o.EmS):-1,fade=t=in:st=0:d=0.3,fade=t=out:st=39.7:d=0.3[em];" +
        "[2]format=gbrp[cv];" +
        "[cv][em]overlay=(W-w)/2:$($o.EmY)[c1];" +
        "[0]scale=$($o.W):$($o.H):force_original_aspect_ratio=increase,crop=$($o.W):$($o.H),gblur=sigma=$BGLUR,eq=brightness=$DARKEN,format=gbrp[bg];" +
        "[bg][c1]blend=all_mode=screen,format=yuv420p[scr];" +
        $flagChain +
        "[$prev]" + ($dt -join ",") + ",scale=$($o.ZS),zoompan=z='1+$($o.Zoom)*on/$( $DUR * $FPS - 1 )':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=$($o.W)x$($o.H):fps=$FPS,gblur=sigma=0.5,noise=alls=5:allf=t,fade=t=in:st=0:d=0.3,fade=t=out:st=39.7:d=0.3[v]"

  if ($o.Name -eq "vertical") { $outPath = Join-Path $VideoDir "$OutBase-vertical.mp4" }
  else { $outPath = Join-Path $VideoDir "$OutBase.mp4" }

  Write-Output "Rendering $outPath ..."
  Set-Content -Path (Join-Path $TmpDir "$($o.Name)_filter.txt") -Value $fc -Encoding UTF8
  $flagArgs = @()
  foreach ($l in $Langs) { if ($l.fp) { $flagArgs += @("-loop", "1", "-framerate", $FPS, "-t", $DUR, "-i", $l.fp) } }
  & ffmpeg -y -v error `
    -loop 1 -framerate $FPS -t $DUR -i $Logo `
    -loop 1 -framerate $FPS -t $DUR -i $Emblem `
    -f lavfi -t $DUR -i "color=black:s=$($o.W)x$($o.H):r=$FPS" `
    -i $Music `
    @flagArgs `
    -filter_complex $fc -map "[v]" -map 3:a `
    -c:v libx264 -pix_fmt yuv420p -r $FPS -c:a copy -shortest -t $DUR `
    $outPath
  if ($LASTEXITCODE -ne 0) { throw "ffmpeg failed for $outPath" }
  Write-Output "Done: $outPath"
}
