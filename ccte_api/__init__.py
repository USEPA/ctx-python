from sys import version_info

from .chemical import Chemical
from .exposure import Exposure

__all__ = ["Chemical", "Exposure"]

if not version_info >= (3,10):
    raise RuntimeError("`ccte_api` needs Python 3.10 or higher.")

print("""
This software/application was developed by the U.S. Environmental Protection Agency 
(USEPA). No warranty expressed or implied is made regarding the accuracy or utility 
of the system, nor shall the act of distribution constitute any such warranty. The 
USEPA has relinquished control of the information and no longer has responsibility 
to protect the integrity, confidentiality or availability of the information. Any 
reference to specific commercial products, processes, or services by service mark, 
trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, 
recommendation or favoring by the USEPA. The USEPA seal and logo shall not be used in 
any manner to imply endorsement of any commercial product or activity by the USEPA or 
the United States Government.""")