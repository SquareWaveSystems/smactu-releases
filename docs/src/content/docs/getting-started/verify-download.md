---
title: Verify your download
description: Check that smactu.vsix matches the SHA256SUMS published with each release.
sidebar:
  order: 2
---

Each release includes a **`SHA256SUMS`** file. Download it alongside
`smactu.vsix`, then compare the hashes.

## Windows

Compare the result of this command with the hash in `SHA256SUMS`:

```powershell
Get-FileHash .\smactu.vsix -Algorithm SHA256
```

## Linux

Run this in the directory containing both files:

```bash
sha256sum --check SHA256SUMS
```

## macOS

```bash
shasum -a 256 --check SHA256SUMS
```

If the hashes do not match, do not install the file. Download it again from the
[Releases page](https://github.com/SquareWaveSystems/smactu-releases/releases),
and [contact support](/support/) if the problem persists.
