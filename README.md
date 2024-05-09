Python wrapper for U.S. EPA's Center for Computational Toxicology and Exposure (CTE) APIs.


```{python}
import ccte_api as cte

c = cte.Chemical()
c.search(by='equals',word='toluene)
```