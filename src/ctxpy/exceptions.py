"""Custom Exceptions for ctx-python"""


class TOMLError(Exception):
    """A base class for TOML errors encounters in ctxpy."""


class TOMLTableExistsError(TOMLError):
    """Error for attempting to change/create existing table in config.toml."""


class TOMLTableNotFoundError(TOMLError):
    """Error for attempting to change non-existant table in config.toml."""
