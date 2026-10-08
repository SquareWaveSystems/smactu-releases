#!/usr/bin/env bash
# Publish an intentional Smactu build to SWS-owned GitHub Releases.
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 || (${2:-} != '' && ${2:-} != --prerelease) ]]; then
  echo 'Usage: publish.sh <file.vsix> [--prerelease]' >&2
  exit 2
fi
artifact=$1
[[ -f $artifact && $artifact == *.vsix ]] || { echo 'Expected an existing .vsix file' >&2; exit 2; }
: "${GH_TOKEN:?Set GH_TOKEN from the SWS_RELEASE_TOKEN CI secret}"
for dependency in gh jq unzip sha256sum; do
  command -v "$dependency" >/dev/null || { echo "Missing dependency: $dependency" >&2; exit 2; }
done

version=$(unzip -p "$artifact" extension/package.json | jq -er '.version | select(type == "string")')
if [[ ! $version =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$ ]]; then
  echo 'VSIX package version must be a semantic version' >&2
  exit 2
fi
version_without_metadata=${version%%+*}
if [[ $version_without_metadata == *-* && ${2:-} != --prerelease ]]; then
  echo 'A prerelease package version requires --prerelease' >&2
  exit 2
fi
tag="v$version"
repository=SquareWaveSystems/smactu-releases
temporary_dir=$(mktemp -d)
trap 'rm -rf "$temporary_dir"' EXIT
cp -- "$artifact" "$temporary_dir/smactu.vsix"
(cd "$temporary_dir" && sha256sum smactu.vsix > SHA256SUMS)

release_flags=()
if [[ ${2:-} == --prerelease ]]; then
  release_flags+=(--prerelease)
fi
gh release create "$tag" "$temporary_dir/smactu.vsix" "$temporary_dir/SHA256SUMS" \
  --repo "$repository" --draft --title "Smactu $version" \
  --notes "Smactu $version. Download smactu.vsix and verify it against SHA256SUMS." \
  "${release_flags[@]}"
if [[ ${2:-} == --prerelease ]]; then
  gh release edit "$tag" --repo "$repository" --draft=false --prerelease --latest=false
else
  gh release edit "$tag" --repo "$repository" --draft=false --latest
fi
printf 'Published: https://github.com/%s/releases/download/%s/smactu.vsix\n' "$repository" "$tag"
