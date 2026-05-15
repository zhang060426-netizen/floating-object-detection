from pathlib import Path


def ensure_within_root(root, target):
    root_path = Path(root).resolve()
    target_path = Path(target).resolve()
    try:
        target_path.relative_to(root_path)
    except ValueError as exc:
        raise ValueError("path escapes storage root") from exc
    return target_path
