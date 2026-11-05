# Convert the Mac (TeachText) manual to a Windows text file: manual.ps1 <in> <out>
param([string]$In, [string]$Out)
$bytes = [IO.File]::ReadAllBytes($In)
$text = [Text.Encoding]::GetEncoding(10000).GetString($bytes) -replace "`r(?!`n)", "`r`n"
[IO.File]::WriteAllText($Out, $text, [Text.Encoding]::UTF8)
