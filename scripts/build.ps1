param(
    [switch]$SkipTests
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $PSScriptRoot
$Venv = Join-Path $Root ".venv"
$Python = Join-Path $Venv "Scripts\python.exe"
$Dist = Join-Path $Root "dist"

Push-Location $Root
try {
    if (-not (Test-Path $Python)) {
        python -m venv $Venv
    }

    & $Python -m pip install --upgrade pip
    & $Python -m pip install -r requirements-dev.txt

    if (-not $SkipTests) {
        & $Python -m pytest
    }

    if (Test-Path $Dist) {
        Remove-Item -LiteralPath $Dist -Recurse -Force
    }

    & $Python -m PyInstaller `
        --noconfirm `
        --clean `
        --onefile `
        --windowed `
        --name runner_stub `
        --collect-all pyfiglet `
        ascii_birthday/runner.py

    $RunnerStub = Join-Path $Dist "runner_stub.exe"
    if (-not (Test-Path $RunnerStub)) {
        throw "runner_stub.exe was not created."
    }

    $AddRunnerStub = "$RunnerStub;."
    & $Python -m PyInstaller `
        --noconfirm `
        --clean `
        --onefile `
        --windowed `
        --name ASCIIBirthdayGenerator `
        "--add-binary=$AddRunnerStub" `
        ascii_birthday/generator.py

    Write-Host ""
    Write-Host "Build complete:"
    Write-Host "  $RunnerStub"
    Write-Host "  $(Join-Path $Dist 'ASCIIBirthdayGenerator.exe')"
}
finally {
    Pop-Location
}
