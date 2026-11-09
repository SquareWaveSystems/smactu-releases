---
title: Install Smactu
description: Download the Smactu VSIX, install it in VS Code and activate your licence.
sidebar:
  order: 1
---

Smactu is distributed as a VSIX file from the
[Releases page](https://github.com/SquareWaveSystems/smactu-releases/releases).
A valid Smactu licence is required to activate the extension.

## Choose a release

- **Stable:** choose the release marked **Latest** for general use.
- **Prerelease:** intended for testers. Use the specific version supplied to you;
  prereleases do not replace the latest stable download.

On the release page, download **`smactu.vsix`**. The automatically generated
"Source code" archives are not the extension installer.

## Install the VSIX

1. Download `smactu.vsix` from the chosen release.
2. In VS Code, open **Extensions**, select the **…** menu, then choose
   **Install from VSIX…** and select the downloaded file.
3. Follow Smactu's licence activation prompts.

Alternatively, if the VS Code command is available in your terminal:

```bash
code --install-extension smactu.vsix
```

See the VS Code documentation on
[installing from a VSIX](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace#_install-from-a-vsix)
for more detail.

:::caution
Keep independent backups of your projects. Validate project changes in Sysmac
Studio before deploying them to equipment.
:::

## Next steps

- [Verify your download](/getting-started/verify-download/) against the published checksum.
