[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$Destination
)

$sourceRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$destinationRoot = [System.IO.Path]::GetFullPath($Destination)

if (Test-Path -LiteralPath $destinationRoot) {
    throw "Destination already exists; choose an empty path: $destinationRoot"
}

New-Item -ItemType Directory -Force -Path $destinationRoot | Out-Null

$files = @(
    'SKILL.md',
    'LICENSE',
    'package.json',
    'package-lock.json'
)

foreach ($relativePath in $files) {
    $sourcePath = Join-Path $sourceRoot $relativePath
    if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
        throw "Required runtime file is missing: $relativePath"
    }
    Copy-Item -LiteralPath $sourcePath -Destination (Join-Path $destinationRoot $relativePath)
}

foreach ($directoryName in @('agents', 'assets', 'references')) {
    $sourcePath = Join-Path $sourceRoot $directoryName
    Copy-Item -LiteralPath $sourcePath -Destination (Join-Path $destinationRoot $directoryName) -Recurse
}

$runtimeScripts = Get-ChildItem -LiteralPath (Join-Path $sourceRoot 'scripts') -File -Filter '*.py'
if (-not $runtimeScripts) {
    throw 'No runtime Python scripts were found.'
}
New-Item -ItemType Directory -Force -Path (Join-Path $destinationRoot 'scripts') | Out-Null
foreach ($script in $runtimeScripts) {
    Copy-Item -LiteralPath $script.FullName -Destination (Join-Path $destinationRoot 'scripts')
}

Write-Output "Runtime skill package created: $destinationRoot"
