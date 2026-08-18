from __future__ import annotations

import base64
import lzma
from pathlib import Path


def read(path: str) -> bytes:
    return b"".join(Path(path).read_bytes().split())


encoded = b"".join(
    (
        read(".deck-build/candidates/chunk-52c249e1"),
        b"d",
        read(".deck-build/payload.part-000"),
        read(".deck-build/candidates/chunk-e2138485"),
        read(".deck-build/candidates/chunk-3ca02c52"),
        read(".deck-build/candidates/chunk-f6da5037"),
    )
)
print(f"Verified base64 prefix length: {len(encoded)}")
raw = base64.b64decode(encoded, validate=True)
print(f"Verified compressed prefix length: {len(raw)}")

decoder = lzma.LZMADecompressor(format=lzma.FORMAT_XZ)
tar_bytes = decoder.decompress(raw)
print(f"Decompressed tar prefix length: {len(tar_bytes)}")
print(f"XZ end reached: {decoder.eof}")
print(f"Unused compressed bytes: {len(decoder.unused_data)}")

position = 0
entry = 0
complete_regular_files = 0
while position + 512 <= len(tar_bytes):
    header = tar_bytes[position : position + 512]
    if header == b"\0" * 512:
        print(f"Zero tar block at offset {position}; stopping.")
        break

    name = header[0:100].split(b"\0", 1)[0].decode("utf-8", "replace")
    prefix = header[345:500].split(b"\0", 1)[0].decode("utf-8", "replace")
    if prefix:
        name = f"{prefix}/{name}"
    size_text = header[124:136].split(b"\0", 1)[0].strip() or b"0"
    try:
        size = int(size_text, 8)
    except ValueError:
        print(f"Invalid tar size at offset {position}: {size_text!r}")
        break
    typeflag = header[156:157] or b"0"
    data_start = position + 512
    padded_size = ((size + 511) // 512) * 512
    next_position = data_start + padded_size
    complete = next_position <= len(tar_bytes)
    print(
        f"{entry:03d} offset={position:09d} type={typeflag!r} "
        f"size={size:7d} complete={complete!s:5s} {name}"
    )
    if complete and typeflag in {b"0", b"\0"}:
        complete_regular_files += 1
    if not complete:
        print(
            f"Incomplete member needs {next_position - len(tar_bytes)} more "
            "decompressed tar bytes."
        )
        break
    position = next_position
    entry += 1

print(f"Complete tar entries: {entry}")
print(f"Complete regular files: {complete_regular_files}")
print(f"Unparsed decompressed bytes: {len(tar_bytes) - position}")
