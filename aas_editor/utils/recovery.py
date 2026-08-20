import json
from pathlib import Path
from typing import Iterable

# Detached tab windows cannot reach the debounce timer via self.window(), so the
# main window registers its scheduler here for edits in any window to trigger it.
_recovery_scheduler = None


def set_recovery_scheduler(cb) -> None:
    global _recovery_scheduler
    _recovery_scheduler = cb


def schedule_recovery_save() -> None:
    if _recovery_scheduler is not None:
        try:
            _recovery_scheduler()
        except RuntimeError:
            # Registered window was destroyed; skip until a live one re-registers,
            # but do not crash the edit that triggered this.
            pass


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


def cleanup_recovery_dir(recovery_dir: Path, keep: Iterable[Path] = ()) -> None:
    """Delete all files in the recovery dir except `keep` (and their .meta.json).

    `keep` holds recovery files of just-restored, not-yet-saved packages; the rest
    (declined, orphaned, leftover .tmp) are swept so the dir does not grow unbounded.
    """
    if not recovery_dir.exists():
        return
    keep_names = set()
    for rec in keep:
        keep_names.add(rec.name)
        keep_names.add(f"{rec.stem}.meta.json")
    for entry in recovery_dir.iterdir():
        if entry.is_file() and entry.name not in keep_names:
            entry.unlink(missing_ok=True)
