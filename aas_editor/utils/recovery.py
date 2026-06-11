import json
from pathlib import Path


def find_recovery_files(recovery_dir: Path) -> dict:
    """Return {original_path: recovery_path} for all valid recovery entries."""
    result = {}
    if not recovery_dir.exists():
        return result
    for meta_file in recovery_dir.glob("*.meta.json"):
        try:
            with open(meta_file, encoding="utf-8") as f:
                meta = json.load(f)
            original = Path(meta["original_path"])
            recovery = recovery_dir / meta["recovery_filename"]
            if recovery.exists():
                result[original] = recovery
        except Exception:
            continue
    return result


def delete_recovery_file(recovery_path: Path) -> None:
    """Delete a recovery data file and its sidecar .meta.json."""
    recovery_path.unlink(missing_ok=True)
    (recovery_path.parent / f"{recovery_path.stem}.meta.json").unlink(missing_ok=True)
