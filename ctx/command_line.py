import argparse
import sys
from pathlib import Path

from .utils import read_env, write_env


def init(x_api_key: str, override: bool=False):
    """
    Initialize the config.toml file for this package, so that a user's API is
    stored and accessed from a centralized location.

    Parameters
    ----------
    x_api_key [string]: personal API key obtained by emailing ccte_api@epa.gov

    override [bool]: if True, override existing API key in .env.ctx file

    """
    data = {
        "host": "https://api-ccte.epa.gov/",
        "accept": "application/json",
        "x-api-key": x_api_key,
    }
    print(f"Override is {override}")

    path = Path.home() / ".env"

    if not path.is_file():
        if not path.parent.is_dir():
            path.parent.mkdir(parents=True, exist_ok=False)

        write_env(data, path)

    else:
        try:
            data = read_env(path)
        except KeyError:
            raise SystemExit(f"{path} does not have x-api-key for CCTE APIs.")
        print(data)
        if not override:
            raise SystemExit(f"Error: x-api-key already exists in {path}. "
                   "Use `--override` to override existing key with passed key.")
        
        data['x-api-key'] = x_api_key
        write_env(data,path)

    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--x-api-key", help="string containing API key")
    parser.add_argument("-s", "--source", help="type of source for data from API")
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
        init(x_api_key=args.x_api_key, override=args.override)
    return
