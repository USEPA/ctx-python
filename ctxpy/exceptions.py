class TOMLError(Exception):
    """A base class for TOML errors encounters in cctepy."""


class TOMLTableExistsError(TOMLError):
    """Error for attempting to change/create existing table in config.toml."""


class TOMLTableNotFoundError(TOMLError):
    """Error for attempting to change non-existant table in config.toml."""
