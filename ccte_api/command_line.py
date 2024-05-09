import toml
import argparse
from pathlib import Path
from ccte_api.exceptions import TableExistsError


def init(x_api_key:str, source:str="public"):
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
    data = {f"{source}_ccte_api":
            {
            "host":"https://api-ccte.epa.gov/",
            "accept":"application/json",
            "x-api-key":x_api_key
            }
        }
    
    path = Path.home() / ".config"
    
    ## There is ~/.config/
    if path.is_dir():
        
        path = path.joinpath('ccte_api')
        
        ## There is ~/.config/ccte_api/
        if path.is_dir():

            path = path.joinpath("config.toml")
            
            ## There is ~/.config/ccte_api/config.toml
            if path.is_file():
                
                ## Read file and if there is a public_ccte_api table
                data = toml.load(path)
                
                if f"{source}_ccte_api" in data.keys():
                    raise TableExistsError(
                        f"Table for`{source}_ccte_api` already exists in "
                        "config.toml, you can manually change the API key, "
                        "if needed.")
                else:
                    with path.open("a") as f:
                        toml.dump(data,f)
            
            ## There is NOT ~/.config/ccte_api/config.toml
            else:
                with path.open("w") as f:
                    toml.dump(data,f)

        ## There is NOT ~/.config/ccte_api/
        else:
            path = path.joinpath("config.toml")
            path.parent.mkdir(parents=True,exist_ok=False)
            
            with path.open('w') as f:
                toml.dump(data,f)
                
    ## There is NOT a .config/ directory in the home directory
    else:
        path = path.joinpath('ccte_api').joinpath("config.toml")
        path.parent.mkdir(parents=True,exist_ok=False)

        with path.open("w") as f:
            toml.dump(data,f)

    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-x','--x-api-key',help="string containing API key")
    parser.add_argument('-s','--source',help="source of ", default="public")
    args = parser.parse_args()
    init(x_api_key=args.x_api_key,source=args.source)
    return