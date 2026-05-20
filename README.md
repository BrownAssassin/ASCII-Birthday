# ASCII-Birthday

ASCII-Birthday is a standalone Windows app for generating personalized birthday executables.

Open the generator, enter a name and age, choose where to save the file, and it creates a standalone `.exe` birthday card that can be sent to someone else. The generated app opens a terminal-style celebration window with large ASCII text, animated ASCII confetti, and closes when any key is pressed.

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

When opened, the generated birthday app displays the age with its ordinal suffix:

```text
Happy [age suffix] Birthday [name]
```

Example: `Happy 21st Birthday Jordan`

in a terminal-style window with large ASCII text and animated ASCII confetti. The window closes when any key is pressed.

## How To Use

1. Open `ASCIIBirthdayGenerator.exe`.
2. Enter the birthday person's name.
3. Enter their age.
4. Choose the output folder.
5. Select `Generate EXE`.
6. Send or open the generated `[name]_[age]_Birthday.exe` file.

The generated birthday file is standalone. It does not need Python, the generator, or any extra files to run.

## Requirements

For normal use:

- Windows 10 or newer
- `ASCIIBirthdayGenerator.exe`

For generated birthday apps:

- Windows 10 or newer
- No installation required

## Notes

- The generated app closes when any key is pressed.
- Names are cleaned automatically so the output filename is valid on Windows.
- Ages must be whole numbers from `1` to `150`.
- Windows SmartScreen may warn when opening unsigned executables. Choose `More info` and `Run anyway` if you trust the file.

## Build From Source

Developers can build the app locally with PowerShell:

```powershell
.\scripts\build.ps1
```

The build script creates a local Python virtual environment, installs pinned dependencies, runs tests, and packages both executables.

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

Run a fresh production build:

```powershell
.\scripts\build.ps1
.\dist\ASCIIBirthdayGenerator.exe
```

## Release Checklist

Use conventional commits when documenting release work:

```text
build: package ascii birthday generator

Package the standalone Windows generator and verify it creates working
personalized birthday executables.
```

Before sharing a release:

- Run `.\scripts\build.ps1`
- Confirm tests pass
- Open `dist\ASCIIBirthdayGenerator.exe`
- Generate a sample birthday executable
- Open the generated birthday executable and confirm it displays the personalized message
