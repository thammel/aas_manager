import sys
import logging
from PyQt6 import QtWidgets

_on_crash_callback = None


def set_crash_callback(cb):
    global _on_crash_callback
    _on_crash_callback = cb


def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Solution from:
    https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python
    - Ignore KeyboardInterrupt so a console python program can exit with Ctrl + C.
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    if _on_crash_callback is not None:
        try:
            _on_crash_callback()
        except Exception:
            pass

    box = QtWidgets.QMessageBox(None)
    box.setIcon(QtWidgets.QMessageBox.Icon.Critical)
    box.setText(f"An Exception was raised. Caught Exception: {exc_value}")
    box.setDetailedText(f"Traceback: {exc_traceback}")
    box.exec()


sys.excepthook = handle_exception
