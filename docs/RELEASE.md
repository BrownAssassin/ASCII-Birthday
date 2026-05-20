# Release Guide

Use this guide when publishing a stable ASCII-Birthday build.

## Repository Metadata

Suggested GitHub description:

```text
Standalone Windows app that generates personalized ASCII birthday executables with animated confetti.
```

Suggested GitHub topics:

```text
ascii-art
birthday
windows
desktop-app
python
tkinter
pyinstaller
executable
generator
gift
```

## Prepare A Stable Build

Run the release prep script:

```powershell
.\scripts\prepare-release.ps1 -Version v1.0.0
```

This script:

- Runs tests
- Builds the runner and generator with PyInstaller
- Copies the distributable app to `release\windows\ASCIIBirthdayGenerator.exe`
- Writes `release\windows\SHA256SUMS.txt`
- Removes temporary build folders and generated samples

Review the result:

```powershell
git status --short
git diff -- README.md docs/RELEASE.md scripts/prepare-release.ps1
```

Commit the release prep:

```powershell
git add README.md docs/RELEASE.md scripts/prepare-release.ps1 release/windows/ASCIIBirthdayGenerator.exe release/windows/SHA256SUMS.txt
git commit -m "chore: prepare v1.0.0 stable release" -m "Refresh the checked-in Windows generator, add release documentation, and include checksums for the distributable app."
git push origin main
```

## Create The GitHub Release

Create and push a tag:

```powershell
git tag -a v1.0.0 -m "ASCII-Birthday v1.0.0"
git push origin v1.0.0
```

On GitHub:

1. Open the repository.
2. Select `Releases`.
3. Select `Draft a new release`.
4. Choose the `v1.0.0` tag.
5. Use the title `ASCII-Birthday v1.0.0`.
6. Attach `release/windows/ASCIIBirthdayGenerator.exe`.
7. Attach `release/windows/SHA256SUMS.txt`.
8. Publish the release.

Suggested release notes are available in `docs/RELEASE_NOTES_v1.0.0.md`.

## Optional Package Asset

For the first release, the GitHub Release asset is the simplest package. You can also attach a zip:

```powershell
Compress-Archive `
  -Path release\windows\ASCIIBirthdayGenerator.exe, release\windows\SHA256SUMS.txt `
  -DestinationPath release\windows\ASCII-Birthday-v1.0.0-windows.zip `
  -Force
```

Attach `release\windows\ASCII-Birthday-v1.0.0-windows.zip` to the GitHub Release.

GitHub Packages is not especially useful for a standalone Windows `.exe` yet. If you want package-manager distribution later, publish the GitHub Release first, then use that public release URL for a WinGet or Chocolatey package.

## GitHub CLI Alternative

If `gh` is installed and authenticated:

```powershell
gh release create v1.0.0 `
  release/windows/ASCIIBirthdayGenerator.exe `
  release/windows/SHA256SUMS.txt `
  --title "ASCII-Birthday v1.0.0" `
  --notes-file docs/RELEASE_NOTES_v1.0.0.md
```
