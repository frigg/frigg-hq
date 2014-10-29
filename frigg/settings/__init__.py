# -*- coding: utf8 -*-
import sys

TESTING = 'test' in sys.argv

# django base settings
from .base import *

# settings variables introduced in frigg
from .frigg import *

try:
    from .local import *
except ImportError, e:
    if not TESTING:
        raise ImportError("Couldn't load local settings frigg.settings.local")

if TESTING:
    from .test import *
