import os
import sys

# On Windows, register torch's lib directory so that c10.dll and its
# sibling DLLs can find each other when the DLL loader resolves imports.
# Without this, PyInstaller bundles work but WinError 1114 is raised at
# runtime because Windows doesn't search _internal/torch/lib/ automatically.
if sys.platform == 'win32' and hasattr(sys, '_MEIPASS'):
    torch_lib = os.path.join(sys._MEIPASS, 'torch', 'lib')
    if os.path.isdir(torch_lib):
        os.add_dll_directory(torch_lib)
