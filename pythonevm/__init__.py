import sys
import pathlib

# ../
script_dir = pathlib.Path(__file__).parent.resolve()

sys.path.append(str(script_dir.absolute()))

from .vm import (
    VM,
)


__version__ = None

__all__ = [
    "__version__",
    "VM",
]