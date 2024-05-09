import toml
from pathlib import Path


path = Path.home().joinpath(".config")
source = "public"
x_api_key = "6f10bec8-1f59-4c19-96af-0eb3aa982613"
override = False
data = {f"{source}_api":
            {
            "host":"https://api-ccte.epa.gov/",
            "accept":"application/json",
            "x-api-key":x_api_key
            }
        }
## There is ~/.config/
if path.is_dir():
    
    path = path.joinpath('ctepy')
    
    ## There is ~/.config/ctepy/
    if path.is_dir():

        path = path.joinpath("config.toml")
        
        ## There is ~/.config/ctepy/config.toml
        if path.is_file():
            
            ## Read file and if there is a public_api table or interal_api
            print("Paths and file exist.")
            data = toml.load(path)
            
            if f"{source}_api" in data.keys():
                ## TODO :Need a way to interact and see if this should be 
                ## overwritten or supply a new table, and then that table 
                ## name needs to passed to the classes.
                pass
            else:
                with path.open("a") as f:
                    toml.dump(data,f)
        
        ## There is NOT ~/.config/ctepy/config.toml
        else:
            print("Child Path exists, but file doesn't")

            with path.open("w") as f:
                toml.dump(data,f)

    ## There is NOT ~/.config/ctepy/
    else:
        print("Parent Path exists, but Child Path and file don't")
        path = path.joinpath("config.toml")
        path.parent.mkdir(parents=True,exist_ok=False)
        
        with path.open('w') as f:
            toml.dump(data,f)
## There is NOT a .config/ directory in the home directory
else:
    print("Parent path and file don't exists")
    
    path = path.joinpath('ctepy').joinpath("config.toml")
    path.parent.mkdir(parents=True,exist_ok=False)

    with path.open("w") as f:
        toml.dump(data,f)