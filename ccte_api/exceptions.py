class TOMLError(Exception):
    """A base class for TOML errors encounters in cctepy."""
    
class TableExistsError(TOMLError):
    """Error for attempting to change/create existing table in config.toml."""
    
class TableNotFoundError(TOMLError):
    """Error for attempting to change non-existant table in config.toml."""