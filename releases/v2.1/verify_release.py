"""Verify this package against its locally trusted checksum inventory. No network or edits."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
ROOT = Path(__file__).resolve().parent

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def verify(root: Path = ROOT) -> dict:
    root = root.resolve()
    errors = []
    expected = {}
    ledger = root / 'release/SHA256SUMS.txt'
    try:
        for line in ledger.read_text(encoding='utf-8').splitlines():
            hash_value, name = line.split('  ', 1)
            rel = PurePosixPath(name)
            if len(hash_value) != 64 or any(c not in '0123456789abcdef' for c in hash_value):
                raise ValueError('Invalid SHA-256 entry')
            if rel.is_absolute() or '..' in rel.parts or name in expected:
                raise ValueError('Unsafe or duplicate ledger path')
            expected[name] = hash_value
            target = root / name
            if target.is_symlink() or not target.resolve().is_relative_to(root):
                errors.append('PATH_ESCAPE_OR_SYMLINK: ' + name)
            elif not target.is_file():
                errors.append('MISSING: ' + name)
            elif digest(target) != hash_value:
                errors.append('HASH_MISMATCH: ' + name)
        actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
        extra = actual - set(expected) - {'release/SHA256SUMS.txt'}
        errors.extend('UNLISTED: ' + n for n in sorted(extra))
        manifest = json.loads((root / 'release/MANIFEST.json').read_text())
        for item in manifest['files']:
            name = item['path']; target = root / name
            if expected.get(name) != item['sha256'] or not target.is_file() or target.stat().st_size != item['bytes']:
                errors.append('MANIFEST_MISMATCH: ' + name)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        errors.append('INVALID_INVENTORY: ' + str(exc))
    return {'status': 'PASS' if not errors else 'FAIL', 'verified_entries': len(expected), 'errors': errors,
            'scope': 'Byte identity against the supplied trusted inventory; no authenticity, evidence-truth or conformance guarantee.'}

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path); args = parser.parse_args()
    result = verify(args.root)
    if args.output:
        if args.output.resolve().is_relative_to(args.root.resolve()):
            parser.error('Write verification evidence outside the immutable publication directory.')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2)); return 0 if result['status'] == 'PASS' else 1
if __name__ == '__main__':
    raise SystemExit(main())
