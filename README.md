# ASCII-Birthday

ASCII-Birthday is a standalone Windows generator for personalized birthday executables.

The generator asks for a name and age, then creates a birthday app named with this scheme:

```text
[name]_[age]_Birthday.exe
```

For example, `Ada Lovelace` turning `36` generates:

```text
Ada_Lovelace_36_Birthday.exe
```

The generated app opens a terminal-style window with large ASCII birthday text, animated ASCII confetti, and closes when any key is pressed.

## Development

Run the tests:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest
```

Run the generator from source after building the runner stub:

```powershell
.\scripts\build.ps1
.\dist\ASCIIBirthdayGenerator.exe
```

## Build

Create both Windows executables:

```powershell
.\scripts\build.ps1
```

Outputs:

```text
dist\runner_stub.exe
dist\ASCIIBirthdayGenerator.exe
```

`ASCIIBirthdayGenerator.exe` is the standalone app to distribute. It contains the reusable runner stub and generates personalized birthday `.exe` files without needing Python on the target machine.

## Checkpoint Commits

Use conventional commits for checkpointed progress:

```text
feat: add birthday payload embedding

Add shared payload writer and reader logic for generated birthday executables.
Validate names and ages, sanitize Windows filenames, and default generated
files to the [name]_[age]_Birthday.exe naming scheme.
```

```text
feat: render personalized ascii birthday window

Add the terminal-style Tkinter runner window with large ASCII birthday text,
animated ASCII confetti, and any-key close behavior.
```

```text
feat: add standalone birthday exe generator

Add the Tkinter generator app that asks for name, age, and output folder,
then creates personalized birthday executables from the embedded runner stub.
```

```text
build: package ascii birthday generator

Add the repeatable PowerShell build workflow that packages runner_stub.exe
and ASCIIBirthdayGenerator.exe with PyInstaller.
```
