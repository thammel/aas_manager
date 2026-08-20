import json
from pathlib import Path

# Detached tab windows are plain TabWidgets, not EditorApp, so a tree view cannot
# reach the debounce timer through self.window(). The main window registers its
# scheduler here so edits in any window trigger a proactive recovery write.
_recovery_scheduler = None


def set_recovery_scheduler(cb) -> None:
    global _recovery_scheduler
    _recovery_scheduler = cb


def schedule_recovery_save() -> None:
    if _recovery_scheduler is not None:
        try:
            _recovery_scheduler()
        except RuntimeError:
            # The registered window was destroyed (e.g. the main window was closed
            # while a detached tab window stayed open). Proactive save is unavailable
            # until a live window re-registers; do not crash the edit that triggered it.
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
