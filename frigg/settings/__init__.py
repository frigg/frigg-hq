# -*- coding: utf8 -*-

# django base settings
from .base import *

# settings variables introduced in frigg
from .frigg import *

try:
    from .local import *
except ImportError, e:
    raise ImportError("Couldn't load local settings frigg.settings.local")
