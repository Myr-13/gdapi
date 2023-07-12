from .level import *
from .local_levels import *
from .utils import *

import os as _os


def lls_path():
	return _os.getenv("localappdata") + "\\GeometryDash\\CCLocalLevels.dat"
