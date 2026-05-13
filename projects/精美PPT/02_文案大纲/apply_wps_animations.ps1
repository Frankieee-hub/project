param(
    [Parameter(Mandatory = $true)]
    [string]$PptPath
)

$ErrorActionPreference = "Stop"

$fullPath = (Resolve-Path -LiteralPath $PptPath).Path
$app = New-Object -ComObject KWPP.Application

try {
    try { $app.Visible = $false } catch {}
    $presentation = $app.Presentations.Open($fullPath)

    # PowerPoint/WPS animation constants. WPS follows the PowerPoint object model here.
    # Reference: Microsoft PowerPoint MsoAnimEffect enumeration.
    $titleEffects = @(23, 10)          # Zoom, Fade
    $bodyEffects = @(10, 22, 2, 30, 34) # Fade, Wipe, Fly, Float, Rise Up
    $closingEffects = @(16, 23)        # Split, Zoom
    $triggerOnClick = 1
    $triggerAfterPrevious = 3

    for ($slideIndex = 1; $slideIndex -le $presentation.Slides.Count; $slideIndex++) {
        $slide = $presentation.Slides.Item($slideIndex)
        $sequence = $slide.TimeLine.MainSequence

        # Remove any stale effects first so repeated runs do not stack animations.
        while ($sequence.Count -gt 0) {
            $sequence.Item(1).Delete()
        }

        $eligible = @()
        for ($shapeIndex = 1; $shapeIndex -le $slide.Shapes.Count; $shapeIndex++) {
            $shape = $slide.Shapes.Item($shapeIndex)

            # Keep backgrounds, card containers, lines, and decorative strips visible.
            # Animate only meaningful text objects so the build order follows the speech.
            $left = [double]$shape.Left
            $top = [double]$shape.Top
            $width = [double]$shape.Width
            $height = [double]$shape.Height
            $area = $width * $height

            $isFullSlide = ($width -gt 880 -and $height -gt 480)
            $isTiny = ($width -lt 25 -or $height -lt 8 -or $area -lt 650)
            $isFooter = ($top -gt 500 -and $height -lt 25)

            $hasText = $false
            $text = ""
            try {
                $hasText = ($shape.HasTextFrame -ne 0 -and $shape.TextFrame.HasText -ne 0)
                if ($hasText) {
                    $text = [string]$shape.TextFrame.TextRange.Text
                    $text = $text.Trim()
                }
            } catch {
                $hasText = $false
            }

            if ($hasText -and $text.Length -gt 0 -and -not $isFullSlide -and -not $isTiny -and -not $isFooter) {
                $priority = 2
                $rowBand = 0
                $colBand = 0
                if ($top -lt 115) {
                    $priority = 0
                }
                elseif ($top -gt 390 -and $width -gt 300) {
                    $priority = 9
                }

                if ($priority -ge 1 -and $priority -lt 9) {
                    # Keep text that belongs to the same visual card/cell together:
                    # title -> subtitle/body, then move to the next card left-to-right.
                    $rowBand = [Math]::Floor([Math]::Max(0, $top - 115) / 135)
                    $colBand = [Math]::Floor([Math]::Max(0, $left) / 160)
                }

                $eligible += [pscustomobject]@{
                    Shape = $shape
                    Priority = $priority
                    RowBand = $rowBand
                    ColBand = $colBand
                    Top = $top
                    Left = $left
                    Width = $width
                    Height = $height
                    Text = $text
                }
            }
        }

        $ordered = @($eligible | Sort-Object Priority, RowBand, ColBand, Top, Left)
        $maxEffects = [Math]::Min($ordered.Count, 16)
        for ($i = 0; $i -lt $maxEffects; $i++) {
            $entry = $ordered[$i]
            $shape = $entry.Shape
            if ($entry.Priority -eq 0) {
                $effectId = $titleEffects[$i % $titleEffects.Count]
            }
            elseif ($entry.Priority -ge 9) {
                $effectId = $closingEffects[$i % $closingEffects.Count]
            }
            else {
                $effectId = $bodyEffects[$i % $bodyEffects.Count]
            }
            $trigger = if ($i -eq 0) { $triggerOnClick } else { $triggerAfterPrevious }
            $effect = $sequence.AddEffect($shape, $effectId, 0, $trigger)
            try { $effect.Timing.Duration = if ($entry.Priority -eq 0) { 0.35 } else { 0.42 } } catch {}
            try { $effect.Timing.TriggerDelayTime = if ($i -eq 0) { 0 } else { 0.08 } } catch {}
        }
    }

    $presentation.Save()
    $presentation.Close()
}
finally {
    try { $app.Quit() } catch {}
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}

Write-Output "WPS animations applied: $fullPath"
