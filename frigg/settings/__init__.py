# -*- coding: utf8 -*-

from frigg.settings.base import *

try:
    from frigg.settings.local import *
except ImportError, e:
    raise ImportError("Couldn't load local settings frigg.settings.local")
