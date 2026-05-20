# ASCII-Birthday

[![Release](https://img.shields.io/github/v/release/BrownAssassin/ASCII-Birthday?display_name=tag&label=release)](https://github.com/BrownAssassin/ASCII-Birthday/releases)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D4?logo=windows&logoColor=white)](#requirements)
[![Python](https://img.shields.io/badge/python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PyInstaller](https://img.shields.io/badge/packaged%20with-PyInstaller-5391FE)](https://pyinstaller.org/)
[![Tests](https://img.shields.io/badge/tests-pytest-0A7F3F)](#development)

ASCII-Birthday is a standalone Windows app for generating personalized birthday executables.

Open the generator, enter a name and age, choose where to save the file, and it creates a standalone `.exe` birthday card that can be sent to someone else. The generated app opens a terminal-style celebration window with large ASCII text, animated ASCII confetti, ordinal ages like `25th`, and closes when any key is pressed.

## Download

For non-developers, use the checked-in Windows app:

```text
release/windows/ASCIIBirthdayGenerator.exe
```

If you are browsing on GitHub, open [`release/windows/ASCIIBirthdayGenerator.exe`](release/windows/ASCIIBirthdayGenerator.exe), select `Download raw file`, then run the downloaded app on Windows.

Once GitHub Releases are published, the recommended download location will be the [latest release](https://github.com/BrownAssassin/ASCII-Birthday/releases/latest).

## How To Use

1. Open `release/windows/ASCIIBirthdayGenerator.exe`.
2. Enter the birthday person's name.
3. Enter their age.
4. Choose the output folder.
5. Select `Generate EXE`.
6. Send or open the generated birthday file.

The generated birthday file is standalone. It does not need Python, the generator, or any extra files to run.

## What It Creates

Generated birthday files use this naming format:

```text
[name]_[age]_Birthday.exe
```

Examples:

```text
Ada_Lovelace_36_Birthday.exe
Anshul_25_Birthday.exe
```

When opened, the generated birthday app displays:

```text
Happy [age suffix] Birthday [name]
```

Example:

```text
Happy 25th Birthday Anshul
```

The birthday window uses large centered ASCII text, animated ASCII confetti, and closes when any key is pressed.

## Requirements

For normal use:

- Windows 10 or newer
- `release/windows/ASCIIBirthdayGenerator.exe`

For generated birthday apps:

- Windows 10 or newer
- No installation required

## Notes

- Names are cleaned automatically so generated filenames are valid on Windows.
- Ages must be whole numbers from `1` to `150`.
- Windows SmartScreen may warn when opening unsigned executables. Choose `More info` and `Run anyway` if you trust the file.
- `release/windows/SHA256SUMS.txt` contains the SHA-256 checksum for the checked-in generator executable.

## Build From Source

Developers can build the app locally with PowerShell:

```powershell
.\scripts\build.ps1
```

Build outputs:

```text
dist\runner_stub.exe
dist\ASCIIBirthdayGenerator.exe
```

`ASCIIBirthdayGenerator.exe` is the app to distribute. It includes `runner_stub.exe` internally and uses it to create personalized birthday executables.

## Development

Run tests directly:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest
```

Prepare the checked-in distributable app for a stable release:

```powershell
.\scripts\prepare-release.ps1 -Version v1.0.0
```

See [docs/RELEASE.md](docs/RELEASE.md) for release steps, package guidance, and suggested GitHub repository metadata.
