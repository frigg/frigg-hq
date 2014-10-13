# -*- coding: utf8 -*-

# django base settings
from frigg.settings.base import *

# settings variables introduced in frigg
from frigg.settings.frigg import *

try:
    from frigg.settings.local import *
except ImportError, e:
    raise ImportError("Couldn't load local settings frigg.settings.local")
