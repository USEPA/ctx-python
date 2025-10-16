"""
ctx-python
=====

Provides a Python interface with EPA's Office of Research and Development, Center for
Computational Toxicology and Exposure's Application Programming Interface (API)
  2. Fast mathematical operations over arrays
  3. Linear Algebra, Fourier Transforms, Random Number Generation

How to use the documentation
----------------------------
Documentation is available in two forms: docstrings provided
with the code.

We recommend exploring the docstrings using
`IPython <https://ipython.org>`_, an advanced Python shell with
TAB-completion and introspection capabilities.  See below for further
instructions.

The docstring examples assume that `ctxpy` has been imported as ctx:

  >>> import ctxpy as ctx

Code snippets are indicated by three greater-than signs::

  >>> c = ctx.Chemical()
  >>> c.search(by='equals',query='toluene')

Use the built-in ``help`` function to view a function's docstring:

  >>> help(ctx.Chemical)

Viewing documentation using IPython
-----------------------------------

Start IPython and import `ctx-python`: `import ctxpy as ctx`. Then, directly paste or 
use the ``%cpaste`` magic to paste examples into the shell. To see which functions are 
available in `ctx-python`, type ``ctx.<TAB>`` (where ``<TAB>`` refers to the TAB key) To 
view the  docstring for a function, use ``ctx.Chemical?<ENTER>`` (to view the docstring) 
and ``ctx.Chemical??<ENTER>`` (to view the source code).

Disclaimer
----------
`ctx-python` was developed by the U.S. Environmental Protection Agency (USEPA). 
No warranty expressed or implied is made regarding the accuracy or utility 
of the system, nor shall the act of distribution constitute any such warranty. The 
USEPA has relinquished control of the information and no longer has responsibility 
to protect the integrity, confidentiality or availability of the information. Any 
reference to specific commercial products, processes, or services by service mark, 
trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, 
recommendation or favoring by the USEPA. The USEPA seal and logo shall not be used in 
any manner to imply endorsement of any commercial product or activity by the USEPA or 
the United States Government.

"""
from sys import version_info
from importlib import metadata

from .chemical import Chemical
from .exposure import Exposure
from .hazard import Hazard
from .chemical_list import ChemicalList

__all__ = ["Chemical", "Exposure","Hazard","ChemicalList"]
__version__ = metadata.version('ctx-python')

_disclaimer = """
`ctx-python` was developed by the U.S. Environmental Protection Agency 
(USEPA). No warranty expressed or implied is made regarding the accuracy or utility 
of the system, nor shall the act of distribution constitute any such warranty. The 
USEPA has relinquished control of the information and no longer has responsibility 
to protect the integrity, confidentiality or availability of the information. Any 
reference to specific commercial products, processes, or services by service mark, 
trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, 
recommendation or favoring by the USEPA. The USEPA seal and logo shall not be used in 
any manner to imply endorsement of any commercial product or activity by the USEPA or 
the United States Government.
"""
if not version_info >= (3,10):
    raise RuntimeError("`ctx-python` needs Python 3.10 or higher.")
