import argparse
import sys
from pathlib import Path
from typing import Optional, Union

from .utils import read_env, write_env

## TODO: CLI tests
def init(ctx_api_x_api_key: str, override: bool=False, env_file: Optional[Union[str,Path]]=None):
    """
    Initialize the .env file for this package, so that a user's API is
    stored and accessed from a centralized location.

    Parameters
    ----------
    x_api_key:string
        personal API key obtained by emailing ccte_api@epa.gov
    override: bool (default False)
        if True, override existing API key in .env file
    env_file: optional, string or pathlib.Path
        name and location of .env file (defaults to ~/.env)

    """
    data = {
        "ctx_api_host": "https://comptox.epa.gov/ctx-api/",
        "ctx_api_accept": "application/json",
        "ctx_api_x_api_key": ctx_api_x_api_key,
    }

    if env_file is None:
        env_file = Path.home() / ".env"

    # Does the file already exist?
    if not env_file.is_file():
        # No, then make it and populate it
        write_env(data, env_file=env_file)

    else:
        # Yes, then read in the env vars in the file
        data = read_env(env_file=env_file)
        
        # Should we override existing keys?
        if override:
            # unset_key(dotenv_path=env_file,key_to_unset='ctx_api_x_api_key')
            data["ctx_api_x_api_key"] = ctx_api_x_api_key
            write_env(data,env_file=env_file)
            
        else:
            # If not add providied key only if key is not in file already
            if 'ctx_api_x_api_key' not in data.keys():
                data["ctx_api_x_api_key"] = ctx_api_x_api_key
                write_env(data,env_file=env_file)
                
            else:
                raise SystemExit(f"Error: ctx_x_api_key variable exists in {env_file}. "
                   "Use `--override` to override existing key with passed key.")

    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--x-api-key", help="string containing API key")
    parser.add_argument(
        "-o",
        "--override",
        action="store_true",
        help="whether to over ride existing API key in file.",
    )
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        init(ctx_api_x_api_key=args.x_api_key, override=args.override)
    return
