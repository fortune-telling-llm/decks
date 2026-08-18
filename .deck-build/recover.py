from __future__ import annotations

import base64
import binascii
import hashlib
import io
import lzma
import re
import subprocess
import tarfile
from pathlib import Path

TARGET_SHA256 = "c5dd8815d7c2f80d4d142c3bff6dff251ca225f60800506076bdc71b51f01676"
XZ_MAGIC = b"\xfd7zXZ\x00"
MAX_NODES = 200_000
BASE64_ALPHABET = bytes(
    dict.fromkeys(b"dABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")
)


def load_chunks() -> tuple[dict[str, bytes], set[str], str]:
    paths = sorted(Path(".deck-build").glob("payload.part-*"))
    paths += sorted(Path(".deck-build/candidates").glob("*"))
    chunks: dict[str, bytes] = {}
    damaged: set[str] = set()
    tiny: list[bytes] = []

    for path in paths:
        data = b"".join(path.read_bytes().split())
        if not data:
            raise RuntimeError(f"Empty payload chunk: {path}")
        if len(data) < 100:
            tiny.append(data)
            continue
        name = path.as_posix()
        chunks[name] = data
        if path.name.startswith("payload.part-"):
            if len(data) != 19_999:
                raise RuntimeError(f"Unexpected damaged chunk size for {path}: {len(data)}")
            damaged.add(name)

    starts = [name for name, data in chunks.items() if data.startswith(b"/Td6WFoAA")]
    if len(starts) != 1:
        raise RuntimeError(f"Expected one archive opening chunk, found {starts!r}")

    print("Recovery inputs:")
    for name, data in chunks.items():
        status = "missing-one-boundary-character" if name in damaged else "complete"
        print(
            f"  {name}: {len(data)} bytes; {status}; "
            f"prefix={data[:16]!r}; suffix={data[-16:]!r}"
        )
    if tiny:
        print(f"  tiny probes retained for character priority: {tiny!r}")

    return chunks, damaged, starts[0]


def inspect_encoded(encoded: bytes) -> tuple[str, bytes | None]:
    if len(encoded) % 4:
        return "invalid", None
    try:
        decoded = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError):
        return "invalid", None
    if not decoded.startswith(XZ_MAGIC):
        return "invalid", None

    decompressor = lzma.LZMADecompressor(format=lzma.FORMAT_XZ)
    try:
        decompressor.decompress(decoded)
    except (lzma.LZMAError, EOFError):
        return "invalid", None

    if not decompressor.eof:
        return "prefix", None
    if decompressor.unused_data:
        return "invalid", None
    if hashlib.sha256(decoded).hexdigest() != TARGET_SHA256:
        return "complete-wrong-hash", decoded
    return "match", decoded


def reconstruct(
    chunks: dict[str, bytes], damaged: set[str], start: str, repair_mode: str
) -> tuple[tuple[tuple[str, str | None], ...], bytes] | None:
    visited = [0]
    accepted = [0]

    start_encoded = chunks[start]
    root_status, root_archive = inspect_encoded(start_encoded)
    if root_status == "invalid":
        raise RuntimeError("The preserved opening chunk is not a valid prefix of an XZ stream.")
    if root_status == "match":
        return ((start, None),), root_archive  # pragma: no cover

    remaining = tuple(name for name in chunks if name != start)

    def search(
        encoded: bytes,
        order: tuple[tuple[str, str | None], ...],
        unused: tuple[str, ...],
    ) -> tuple[tuple[tuple[str, str | None], ...], bytes] | None:
        visited[0] += 1
        if visited[0] > MAX_NODES:
            raise RuntimeError(f"Repair search exceeded {MAX_NODES} nodes.")

        choices = sorted(
            unused,
            key=lambda name: (
                name in damaged,
                -len(chunks[name]),
                name,
            ),
        )
        for name in choices:
            raw = chunks[name]
            repairs: tuple[int | None, ...]
            if name in damaged:
                repairs = tuple(BASE64_ALPHABET)
            else:
                repairs = (None,)

            for repair in repairs:
                if repair is None:
                    piece = raw
                    repair_text = None
                elif repair_mode == "append":
                    piece = raw + bytes((repair,))
                    repair_text = chr(repair)
                elif repair_mode == "prepend":
                    piece = bytes((repair,)) + raw
                    repair_text = chr(repair)
                else:  # pragma: no cover
                    raise AssertionError(repair_mode)

                candidate = encoded + piece
                status, archive = inspect_encoded(candidate)
                if status == "invalid" or status == "complete-wrong-hash":
                    continue

                accepted[0] += 1
                print(
                    f"Accepted XZ prefix #{accepted[0]} at depth {len(order) + 1}: "
                    f"{name} repair={repair_text!r} status={status}",
                    flush=True,
                )
                next_order = order + ((name, repair_text),)
                if status == "match":
                    assert archive is not None
                    print(
                        f"Matched after {visited[0]} search nodes and "
                        f"{accepted[0]} accepted prefixes using {repair_mode} repair."
                    )
                    return next_order, archive

                next_unused = tuple(item for item in unused if item != name)
                result = search(candidate, next_order, next_unused)
                if result is not None:
                    return result
        return None

    result = search(start_encoded, ((start, None),), remaining)
    print(
        f"Mode {repair_mode!r} exhausted after {visited[0]} nodes and "
        f"{accepted[0]} accepted prefixes."
    )
    return result


def validate_and_extract(archive: bytes) -> None:
    actual = hashlib.sha256(archive).hexdigest()
    if actual != TARGET_SHA256:
        raise RuntimeError(f"Archive checksum mismatch: {actual}")
    lzma.decompress(archive, format=lzma.FORMAT_XZ)

    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as deck_tar:
        members = deck_tar.getmembers()
        for member in members:
            member_path = Path(member.name)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise RuntimeError(f"Unsafe archive member: {member.name}")
        deck_tar.extractall(path=".", filter="data")

    root = Path("tarot/stellar-mosaic-tarot")
    files = sorted(
        root.glob("[0-9]*.md"),
        key=lambda path: int(path.name.split("-", 1)[0]),
    )
    if len(files) != 78:
        raise RuntimeError(f"Expected 78 card files, found {len(files)}")
    indices = [int(path.name.split("-", 1)[0]) for path in files]
    if indices != list(range(1, 79)):
        raise RuntimeError(f"Non-continuous card indices: {indices}")
    for required_path in (
        root / "1-ace-of-wands.md",
        root / "78-the-world.md",
        root / "DECK-INFO.md",
    ):
        if not required_path.is_file():
            raise RuntimeError(f"Missing required file: {required_path}")

    required_headings = (
        "## Card metadata",
        "## Literal visual description",
        "## Core meaning",
        "### Upright keywords",
        "### Reversed / shadow keywords",
        "## Symbol-by-symbol interpretation",
        "## Divinatory interpretation by question type",
        "## Intentions",
        "## Feelings",
        "## Actions / likely next move",
        "## Advice",
        "## Outcome",
        "## Yes / no",
        "## Timing",
        "## Health / wellbeing readings",
        "## Spread interactions",
        "## Image-led reading examples",
        "## Fortune-teller cautions",
        "## One-sentence essence",
    )
    forbidden = re.compile(
        r"placeholder|lorem ipsum|(^|[^A-Z])TBD([^A-Z]|$)|(^|[^A-Z])TODO([^A-Z]|$)",
        re.I,
    )
    titles: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        first = text.splitlines()[0]
        if not first.startswith("# "):
            raise RuntimeError(f"{path}: missing title")
        titles.append(first)
        for heading in required_headings:
            if heading not in text:
                raise RuntimeError(f"{path}: missing {heading}")
        if forbidden.search(text):
            raise RuntimeError(f"{path}: placeholder marker found")
        symbol_sections = len(re.findall(r"^### .+ — .+$", text, re.M))
        if symbol_sections < 5:
            raise RuntimeError(f"{path}: fewer than five card-specific symbol sections")

    if len(set(titles)) != 78:
        raise RuntimeError("Duplicate card titles found")
    for suit in ("wands", "cups", "swords", "pentacles"):
        count = sum(1 for path in files if f"-of-{suit}.md" in path.name)
        if count != 14:
            raise RuntimeError(f"Expected 14 {suit} cards, found {count}")

    subprocess.run(["xz", "--test", "/tmp/stellar-mosaic.tar.xz"], check=True)
    print("Validated 78 continuous, unique, fully structured card descriptions.")


def main() -> None:
    chunks, damaged, start = load_chunks()
    expected_length = sum(len(data) for data in chunks.values()) + len(damaged)
    print(f"Expected repaired base64 length: {expected_length}")
    if expected_length != 131_000:
        raise RuntimeError(f"Unexpected repaired payload length: {expected_length}")

    result = reconstruct(chunks, damaged, start, "append")
    if result is None:
        result = reconstruct(chunks, damaged, start, "prepend")
    if result is None:
        raise RuntimeError("No checksum-valid XZ archive was found after bounded boundary repair.")

    order, archive = result
    Path("/tmp/stellar-mosaic.tar.xz").write_bytes(archive)
    print(f"Archive size: {len(archive)} bytes")
    print(f"Archive SHA-256: {hashlib.sha256(archive).hexdigest()}")
    print("Recovered order and boundary characters:")
    for index, (name, repair) in enumerate(order):
        print(f"  {index:02d}: {name}; repair={repair!r}")

    validate_and_extract(archive)


if __name__ == "__main__":
    main()
