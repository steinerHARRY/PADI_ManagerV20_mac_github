# PADI Manager macOS build

This repository builds `PADI Manager.app` on GitHub-hosted macOS runners.

## Build

1. Open the repository on GitHub.
2. Open **Actions**.
3. Select **Build PADI Manager macOS**.
4. Click **Run workflow** and choose `main`.
5. When both jobs finish, download one of the artifacts:
   - `PADI-Manager-Apple-Silicon` for Apple Silicon Macs.
   - `PADI-Manager-Intel` for Intel Macs.

The workflow builds with Python 3.13 and PyInstaller in `--onedir --windowed` mode.

## Runtime data

On macOS, writable data is stored outside the app bundle in:

`~/Library/Application Support/PADI Manager/`

This includes instructor data, state, comments, signatures, and cached PDF templates.

## First-launch note

The workflow uses ad-hoc signing for test builds. It does not perform Apple Developer ID signing or notarization. macOS Gatekeeper can therefore warn when the app is first opened after download.
