from pathlib import Path
from typing import Optional, Union

from dotenv import dotenv_values, set_key


def chunker(listlike, size):
    """
    Iterator that provides shorthand for iterating over a sequence on chunck (of length
    size) at a time.
    
    Parameters
    ----------
    listlike: list-like
        a list-like object that needs to be divided into smaller chuncks
    size: integer
        the number of items that should be in each chunk
    
    Returns
    -------
    generator
    """
    return (listlike[pos : pos + size] for pos in range(0, len(listlike), size))


def flatten(lofl:list):
    """
    Takes a list of lists into and flattens into a single list
    
    Parameters
    ----------
    lofl : list
        list of lists that needs to be flatted
        
    Returns
    -------
    list
    
    Examples
    --------
    >>> l = [[1,2,3],[0,9,8]]
    >>> flatten(l)
    ... [1,2,3,0,9,8]
    """
    return [item for lst in lofl for item in lst]


def write_env(data:dict, env_file: Optional[Union[str, Path]] = None):
    """
    Writes or appends environment variables to a .env file. If no file exists,
    one is created.
    
    Parameters
    ----------
    data : dict
        Dictionary of key-value pairs where each key is the name of an environment
        variable and each value is the value of the environment variable.
    env_file : str or pathlib.Path
        File that environment variable information should be written to.

    """
    if env_file is None:
        env_file = Path.home() / ".env"
    for k, v in data.items():
        print("this is the write_env call",k,v)
        set_key(env_file, k, v)
    return


def read_env(env_file: Optional[Union[str, Path]] = None):
    """
    Read environment variable information from file
    
    Parameters
    ----------
    env_file : str or pathlib.Path
        File that environment variable information should be read from.
        
    Returns
    -------
    dict
        Dictionary of key-value pairs where each key is the name of an environment
        variable and each value is the value of the environment variable.
    """
    if env_file is None:

        ## Standard path to .env file
        env_file = Path.home() / ".env"

    if not env_file.is_file():
        raise FileNotFoundError(f"{env_file.as_posix()} does not exist.")

    config = dotenv_values(env_file)
    # config = {"-".join(k.lower().split("_")[2:]):v for k,v in config.items()}

    # if "x-api-key" not in config.keys():
    #     raise KeyError(f"x-api-key not found in {env_file.as_posix()} file.")

    return config