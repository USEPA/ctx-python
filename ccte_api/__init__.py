from sys import version_info

from .chemical import Chemical
from .exposure import Exposure

__all__ = ['Chemical',
           'Exposure']

if version_info.major < 3:
    raise RuntimeError("`dsstox` needs Python 3.10 or higher.")

if version_info.minor < 10:
    raise RuntimeError("`dsstox` needs Python 3.10 or higher.")
