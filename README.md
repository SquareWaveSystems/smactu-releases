# Smactu downloads

**Smactu** is a Visual Studio Code extension for working with Omron Sysmac Studio
projects. This is the official download repository maintained by
[Square Wave Systems](https://squarewavesystems.com.au).

## Availability

No builds have been published here yet. Downloads will appear on the
[Releases page](https://github.com/SquareWaveSystems/smactu-releases/releases)
when available. A valid Smactu licence is required to activate the extension.

## Choose a release

- **Stable:** choose the release marked **Latest** for general use.
- **Prerelease:** intended for testers. Use the specific version supplied to you;
  prereleases do not replace the latest stable download.

Published releases, including prereleases, are publicly downloadable.

On the release page, download **`smactu.vsix`**. The automatically generated
“Source code” archives are not the extension installer.

## Install

1. Download `smactu.vsix` from the chosen release.
2. In VS Code, open **Extensions**, select the **…** menu, then choose
   **Install from VSIX…** and select the downloaded file.
3. Follow Smactu's licence activation prompts.

Alternatively, if the VS Code command is available in your terminal:

```bash
code --install-extension smactu.vsix
```

Keep independent backups of your projects. Validate project changes in Sysmac
Studio before deploying them to equipment.

## Verify your download

Each release also includes **`SHA256SUMS`**. Download it alongside the VSIX.

On Windows, compare the result of this command with the hash in `SHA256SUMS`:

```powershell
Get-FileHash .\smactu.vsix -Algorithm SHA256
```

On Linux, run this in the directory containing both files:

```bash
sha256sum --check SHA256SUMS
```

On macOS:

```bash
shasum -a 256 --check SHA256SUMS
```

## Support and feedback

- **Bugs and feature requests:** [Smactu feedback](https://github.com/SquareWaveSystems/smactu-feedback/issues).
- **Licensing, billing or private support:** [support@squarewavesystems.com.au](mailto:support@squarewavesystems.com.au).
- **Product information:** [Square Wave Systems](https://squarewavesystems.com.au).

Include your Smactu version, VS Code version, operating system and steps to
reproduce a problem. Keep licence keys, credentials and confidential project
files out of public reports.
