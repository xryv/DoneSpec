from __future__ import annotations

from pathlib import Path


def resolve_under_root(root_dir: Path, raw_path: str) -> Path:
    """Resolve a user path under the validation root without escaping it."""
    root = root_dir.resolve()
    target = (root / raw_path).resolve()

    try:
        target.relative_to(root)
    except ValueError as exc:
        msg = f"Path escapes validation root: {raw_path}"
        raise ValueError(msg) from exc

    return target
