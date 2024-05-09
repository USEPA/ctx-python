from sys import version_info
from pathlib import Path

from .chemical import Chemical
from . import hazard
from . import bioactivity
from .exposure import Exposure
from . import ecotox



if version_info.major < 3:
    raise RuntimeError("`dsstox` needs Python 3.10 or higher.")

if version_info.minor < 10:
    raise RuntimeError("`dsstox` needs Python 3.10 or higher.")
