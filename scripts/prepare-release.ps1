param(
    [string]$Version = "v1.0.0"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $PSScriptRoot
$ReleaseDir = Join-Path $Root "release\windows"
$ReleaseExe = Join-Path $ReleaseDir "ASCIIBirthdayGenerator.exe"
$ChecksumFile = Join-Path $ReleaseDir "SHA256SUMS.txt"

function Remove-WorkspacePath {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }

    $RootPath = (Resolve-Path -LiteralPath $Root).Path
    $TargetPath = (Resolve-Path -LiteralPath $Path).Path
    if (-not ($TargetPath -eq $RootPath -or $TargetPath.StartsWith("$RootPath\"))) {
        throw "Refusing to remove path outside workspace: $TargetPath"
    }

    Remove-Item -LiteralPath $TargetPath -Recurse -Force
}

Push-Location $Root
try {
    & (Join-Path $PSScriptRoot "build.ps1")

    New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null
    Copy-Item -LiteralPath (Join-Path $Root "dist\ASCIIBirthdayGenerator.exe") -Destination $ReleaseExe -Force

    $Hash = (Get-FileHash -LiteralPath $ReleaseExe -Algorithm SHA256).Hash.ToLowerInvariant()
    Set-Content -LiteralPath $ChecksumFile -Value "$Hash  ASCIIBirthdayGenerator.exe" -Encoding ascii

    Remove-WorkspacePath (Join-Path $Root "build")
    Remove-WorkspacePath (Join-Path $Root "dist")
    Remove-WorkspacePath (Join-Path $Root "generated")
    Remove-WorkspacePath (Join-Path $Root ".pytest_cache")
    Remove-WorkspacePath (Join-Path $Root "ASCIIBirthdayGenerator.spec")
    Remove-WorkspacePath (Join-Path $Root "runner_stub.spec")

    foreach ($CacheDir in Get-ChildItem -Path @("ascii_birthday", "tests") -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue) {
        Remove-WorkspacePath $CacheDir.FullName
    }

    Write-Host ""
    Write-Host "Release prepared for ${Version}:"
    Write-Host "  $ReleaseExe"
    Write-Host "  $ChecksumFile"
}
finally {
    Pop-Location
}
