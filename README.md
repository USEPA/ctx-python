# ctx-python

Python wrapper for U.S. EPA's Center for Computational Toxicology and Exposure (CTE) APIs.


## Installation
`ctx-python` is available to install via `pip`.

```
pip install ctx-python
```


## Initialization
**Before being able to access CCTE's API, a user must acquire an API key.** See [https://www.epa.gov/comptox-tools/computational-toxicology-and-exposure-apis-about](https://www.epa.gov/comptox-tools/computational-toxicology-and-exposure-apis-about) for more information.

Once an API key is obtained, `ctx-python` offers two options for passing the key for authentication:

1. Supply the key at the point of instantiatation for each domain. This will look something like:

```{python}
import ctxpy as ctx

chem = ctx.Chemical(x_api_key='648a3d70')
```

2. `ctx-python` comes with a command-line tool that will utilize the `.env` file that will store the key. If no key is supplied at instantiation, `ctx-python` will automatically attempt to load this file and use a key stored there.
```{bash}
[user@host~]$ ctx_init --x-api-key 648a3d70
```
This will result in the .env file having three new environment variables added to the file: `ctx_api_host`, `ctx_api_accept`, `ctx_x_api_key`.

```{python}
import ctxpy as ctx

chem = ctx.Chemical()
```


## Usage
The backbone of `ctx-python` is its base `Connection` class. This class takes the appropriate authentication key and other important information for GET and POST commands and stores them for each call to the API. There are 5 different domains that have a specific `Connection` sub-class:
- Chemical
- Chemical Lists (limited functionality)
- Exposure
- Hazard



### Chemical
The `Chemical` class provides capabilities to:
- search for chemicals by their names, CAS-RNs, DTXSIDs, or other potential identifiers
- retrieve details about a chemical from a DTXSID (single chemical or batch search) or DTXCID (single chemical only)
- search for chemicals that match features common in Mass Spectrometry (i.e., a range of molecular mass, chemical formula, or by DTXCID)

```{python}
import ctx

# Start an instance of the Chemical class
chem = ctx.Chemical()

# Search for some data
chem.search(by='equals', query='toluene')
chem.search(by='starts-with', query='atra')
chem.search(by='contains', query='-00-')
chem.search(by='batch', query=['50-00-0','BPA'])


# Get some chemical details
chem.details(by='dtxsid', query='DTXSID7020182')
chem.details(by='dtxcid', query='DTXCID701805')
chem.details(by='batch', query=['DTXSID7020182','DTXSID3021805'])

# Search for some MS info
chem.msready(by='dtxcid', query='DTXCID30182')
chem.msready(by='formula', query='C17H19NO3')
chem.msready(by='mass', start=200.9, end=200.93)
```


### Exposure
The `Exposure` class provides capabilities to search EPA's Chemical and Products Database (CPDat), High-throughput Toxicokinetics data (httk), and return predictions from its Quantitative Structure-Use Relationship (QSUR) models and from Systematic Empirical Evaluation of Models (SEEM) framework for exposure predictions.


```{python}
import ctx

# Start an instance of the Exposure class
expo = ctx.Exposure()

# Search for data reported data from CPDat
expo.search_cpdat(vocab_name="fc", dtxsid="DTXSID7020182")
expo.search_cpdat(vocab_name='puc', dtxsid='DTXSID7020182')
expo.search_cpdat(vocab_name='lpk', dtxsid='DTXSID7020182')

# Get httk data results
expo.search_httk(dtxsid='DTXSID7020182')

# Get controlled vocabularies from CPDat
expo.get_cpdat_vocabulary(vocab_name='fc')
expo.get_cpdat_vocabulary(vocab_name='puc')
expo.get_cpdat_vocabulary(vocab_name='lpk')

# Get predictions of functional use
expo.search_qsur(dtxsid='DTXSID7020182')

# Get exposure pathway predictions
expo.search_exposures(by='pathways',dtxsid='DTXSID7020182')

# Get exposure estimates from SEEM framework
expo.search_exposures(by='seem',dtxsid='DTXSID7020182')
```

With all search methods in the Exposure class, it is possible to provide a list of DTXSIDs and receive back a pandas DataFrame for all submitted chemicals in the list.

```{python}
expo.search_qsurs(dtxsid=['DTXSID7020182','DTXSID3021805'])
```


## Hazard
The `Hazard` class provides capabilities to access all hazard endpoints from the CTX APIs. These endpoints provide access to EPA's Toxicity Values Database (ToxValDB) and other data sources used by EPA's Office of Research and Development.

```{python}
import ctxpy as ctx

haz = ctx.Hazard()

## Search ToxValDB for cancer data on specific chemical
haz.search_toxvaldb(by='cancer', dtxsid='DTXSID7020182')

## Search ToxValDB for all chemical's human data
haz.search(by='human',dtxsid='DTXSID7020182')

## Search ToxValDB for all chemical's ecological data
haz.search(by='eco',dtxsid='DTXSID7020182')

## Search chemical's skin/eye irritant data
haz.search(by='skin-eye',dtxsid='DTXSID7020182')

## Search chemical's cancer data
haz.search(by='cancer',dtxsid='DTXSID7020182')

## Search chemical's genetic toxicity data (summary data only )
haz.search(by='genetox',dtxsid='DTXSID7020182')

## Search chemical's genetic toxicity detailed data
haz.search(by='genetox',dtxsid='DTXSID7020182',summary=False)
```

Explicit batch searching is also available for the `Hazard` class.
```{python}
haz.batch_search(by='human',dtxsid=['DTXSID7020182','DTXSID3021805'])
```


## Disclaimer
This software/application was developed by the U.S. Environmental Protection Agency (USEPA). No warranty expressed or implied is made regarding the accuracy or utility of the system, nor shall the act of distribution constitute any such warranty. The USEPA has relinquished control of the information and no longer has responsibility to protect the integrity, confidentiality or availability of the information. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the USEPA. The USEPA seal and logo shall not be used in any manner to imply endorsement of any commercial product or activity by the USEPA or the United States Government.
