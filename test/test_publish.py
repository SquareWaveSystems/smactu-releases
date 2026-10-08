import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "publish.sh"


class PublishTests(unittest.TestCase):
    def run_publish(self, version="1.2.3", prerelease=False, fail_create=False, manifest=True):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact = root / "input with spaces.vsix"
            with zipfile.ZipFile(artifact, "w") as archive:
                archive.writestr("extension/package.json", json.dumps({"version": version}) if manifest else "bad json")
            expected_hash = hashlib.sha256(artifact.read_bytes()).hexdigest()
            log = root / "gh.jsonl"
            gh = root / "gh"
            gh.write_text('''#!/usr/bin/env python3
import hashlib, json, os, pathlib, sys
args = sys.argv[1:]
record = {"args": args}
if args[:2] == ["release", "create"]:
    assets = [pathlib.Path(arg) for arg in args[3:] if pathlib.Path(arg).is_file()]
    record["assets"] = [p.name for p in assets]
    record["checksum"] = next(p.read_text() for p in assets if p.name == "SHA256SUMS")
    record["hash"] = hashlib.sha256(next(p for p in assets if p.name == "smactu.vsix").read_bytes()).hexdigest()
with open(os.environ["GH_TEST_LOG"], "a") as stream:
    stream.write(json.dumps(record) + "\\n")
if args[:2] == ["release", "create"] and os.environ.get("FAIL_CREATE") == "1":
    sys.exit(1)
''')
            gh.chmod(0o755)
            environment = dict(os.environ, PATH=f"{root}:{os.environ['PATH']}", GH_TOKEN="synthetic-test-token", GH_TEST_LOG=str(log), FAIL_CREATE="1" if fail_create else "0")
            command = ["bash", str(SCRIPT), str(artifact)]
            if prerelease:
                command.append("--prerelease")
            result = subprocess.run(command, cwd=root, env=environment, capture_output=True, text=True)
            calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
            return result, calls, expected_hash

    def test_stable_publishes_both_verified_assets_before_becoming_latest(self):
        result, calls, expected_hash = self.run_publish()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(calls), 2)
        self.assertIn("--draft", calls[0]["args"])
        self.assertEqual(calls[0]["args"][2], "v1.2.3")
        self.assertEqual(calls[0]["assets"], ["smactu.vsix", "SHA256SUMS"])
        self.assertEqual(calls[0]["hash"], expected_hash)
        self.assertEqual(calls[0]["checksum"], f"{expected_hash}  smactu.vsix\n")
        self.assertIn("--draft=false", calls[1]["args"])
        self.assertIn("--latest", calls[1]["args"])
        self.assertIn("SquareWaveSystems/smactu-releases", calls[0]["args"])

    def test_tester_build_cannot_replace_latest_stable(self):
        for version in ["1.2.3", "1.2.3-beta.1+build.7"]:
            with self.subTest(version=version):
                result, calls, _ = self.run_publish(version, prerelease=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("--prerelease", calls[0]["args"])
                self.assertIn("--prerelease", calls[1]["args"])
                self.assertIn("--latest=false", calls[1]["args"])

    def test_stable_build_metadata_can_contain_hyphens(self):
        result, calls, _ = self.run_publish("1.2.3+build-7")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--latest", calls[1]["args"])

    def test_duplicate_or_failed_upload_never_publishes(self):
        result, calls, _ = self.run_publish(fail_create=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(calls), 1)

    def test_prerelease_version_needs_explicit_channel(self):
        result, calls, _ = self.run_publish("1.2.3-beta.1")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(calls, [])

    def test_bad_version_or_manifest_never_contacts_github(self):
        for version, manifest in [("../bad", True), ("01.2.3", True), (None, True), ("1.2.3", False)]:
            with self.subTest(version=version, manifest=manifest):
                result, calls, _ = self.run_publish(version, manifest=manifest)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
