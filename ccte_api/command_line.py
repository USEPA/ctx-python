import toml
import argparse
from pathlib import Path
from ccte_api.exceptions import TOMLTableExistsError


def init(x_api_key: str, source: str = "public"):
    """
    Initialize the config.toml file for this package, so that a user's API is
    stored and accessed from a centralized location.

    Parameters
    ----------
    x_api_key [string]: personal API key obtained by emailing ccte_api@epa.gov

    source [string="public|internal"]: the source of data being called from the
    API."public" means the data have been released to the public. This is the
    option for most users. EPA employees, behing the firewall will, in the
    future, have access to an internal data source and can use the "internal"
    source parameter.

    """
    data = {
        f"{source}_ccte_api": {
            "host": "https://api-ccte.epa.gov/",
            "accept": "application/json",
            "x-api-key": x_api_key,
        }
    }

    path = Path.home() / ".config" / "ccte_api" / "config.toml"

    if not path.is_file():
        if not path.parent.is_dir():
            path.parent.mkdir(parents=True, exist_ok=False)

        with path.open("w") as f:
            toml.dump(data, f)

    else:
        data = toml.load(path)

        if f"{source}_ccte_api" in data.keys():
            raise TOMLTableExistsError(
                f"Table for`{source}_ccte_api` already exists in "
                f"{path.as_posix()}, you can manually change the API key, "
                "if needed."
            )
        else:
            with path.open("a") as f:
                toml.dump(data, f)

    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--x-api-key", help="string containing API key")
    parser.add_argument(
        "-s", "--source", help="type of source for data from API", default="public"
    )
    args = parser.parse_args()
    init(x_api_key=args.x_api_key, source=args.source)
    return
