# isort: dont-add-imports
from __future__ import annotations

from datetime import date
from importlib import metadata

__title__ = "aiordr"
__author__ = "Nice Aesthetics"
__license__ = "GPLv3+"
__copyright__ = f"Copyright {date.today().year} {__author__}"

from . import exceptions
from . import helpers
from . import models
from .client import *

__all__ = (
    "exceptions",
    "helpers",
    "models",
    "ordrClient",
)

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    import toml

    __version__ = toml.load("pyproject.toml")["tool"]["poetry"]["version"] + "dev"
