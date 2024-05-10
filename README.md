# ccte_api

Python wrapper for U.S. EPA's Center for Computational Toxicology and Exposure (CTE) APIs.

## Installation
Coming soon...

## Initialization
Before being able to access CCTE's API, a use must acquire an API key. See [https://api-ccte.epa.gov/docs/](https://api-ccte.epa.gov/docs/) for more information.

Once an API key is obtained, `ccte_api` offers two options for passing the key for authentication:

1. Supply the key at the point of instantiatation for each domain. This will look something like:

```{python}
import ccte_api as cte

chem = cte.Chemical(x_api_key='648a3d70')
```

2. `ccte_api` comes with a command-line tool that will create a `config.toml` file that will store the key. If no key is supplied at instantiation, `ccte_api` will automatically attempt to load this file and use a key stored there.
```{bash}
[user@host~]$ ccte_init --x-api-key 648a3d70
```

## Usage
The backbone of `ccte_api` is its base `Connection` class. This class takes the appropriate authentication key and other important information for GET and POST commands and stores them for each call to the API. There are 5 different domains that have a specific `Conncetion` sub-class:
- Chemical
- Exposure
- Hazard
- Bioactivity
- Ecotox

