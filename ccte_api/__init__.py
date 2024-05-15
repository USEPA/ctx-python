from sys import version_info

from .chemical import Chemical
from .exposure import Exposure

__all__ = ["Chemical", "Exposure"]

if not version_info >= (3,10):
    raise RuntimeError("`ccte_api` needs Python 3.10 or higher.")

