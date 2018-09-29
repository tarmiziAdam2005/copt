__version__ = '0.4.0-dev'

from .proxgrad import minimize_PGD, minimize_APGD
from .splitting import minimize_TOS, minimize_PDHG
from .randomized import minimize_SAGA_L1, minimize_SVRG_L1, minimize_VRTOS
from .frank_wolfe import minimize_FW, minimize_PFW_L1
from . import datasets
from . import tv_prox
from . import utils
