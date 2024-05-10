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

### Chemicals
The chemical domain provides capabilities to:
- search for chemicals by their names, CAS-RNs, DTXSIDs, or other potential identifiers
- retrieve details about a chemical from a DTXSID (single chemical or batch search) or DTXCID (single chemical only)
- search for chemicals that match features common in Mass Spectrometry (i.e., a range of molecular mass, chemical formula, or by DTXCID)
```{python}
import ccte_api as cte

## Start an instance of the Chemical class
chem = cte.Chemical()

## Search for some data
chem.search(by='equals",word='toluene')
chem.search(by='starts-with',word='atra')
chem.search(by='contains',word='-00-')
chem.search(by='batch',word=['50-00-0','BPA'])


## Get some chemical details
chem.details(by='dtxsid', word='DTXSID7020182')
chem.details(by='dtxcid', word='DTXCID701805')
chem.details(by='batch', word=['DTXSID7020182','DTXSID3021805'])

## Search for some MS info
chem.msready(by='dtxcid',word='DTXCID30182')
chem.msready(by='formula', word='C17H19NO3')
chem.msready(by='mass', start=200.9, end=200.93)
```

### Exposure
The exposure domain provides capabilities to:
- search for a chemical's:
    - reported functional use information
    - predicted functional uses
    - presence in consumer/industrial formulations or articles
    - presence in annotated chemical list
- retrieve controlled vocabularies for:
    - Function Categories (FC)
    - Product Use Categories (PUC)
    - List Presence Keywords (LPKs)
```{python}
import ccte_api as cte

## Start an instance of the Exposure class
expo = cte.Exposure()

## Search for some data
expo.search(by="fc",word="DTXSID7020182")
expo.search(by='qsur',word='DTXSID7020182')
expo.search(by='puc',word='DTXSID7020182')
expo.search(by='lpk', word='DTXSID7020182')


## Get controlled vocabularies
expo.vocabulary(by='fc')
expo.vocabulary(by='puc')
expo.vocabulary(by='lpk')
```