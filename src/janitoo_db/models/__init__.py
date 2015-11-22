# -*- coding: utf-8 -*-
__license__ = """

This file is part of **janitoo** project https://github.com/bibi21000/janitoo.

License : GPL(v3)

**janitoo** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**janitoo** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with janitoo. If not, see http://www.gnu.org/licenses.
"""
__copyright__ = "Copyright © 2013-2014 Sébastien GALLET aka bibi21000"
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
import logging
logger = logging.getLogger( "janitoo.db" )
try:
    __import__('pkg_resources').declare_namespace(__name__)
except:  # pragma: no cover
    # bootstrapping
    pass # pragma: no cover

import sys
from os.path import dirname, basename, isfile
import glob
modules = [ basename(f)[:-3] for f in glob.glob(dirname(__file__)+"/*.py") if isfile(f) and not basename(f).startswith('_')]
logger.info("Load core models %s", modules)
for module in modules:
    #~ __import__(module, locals(), globals())
    mod = __import__(module, locals(), globals())
    mod.extend(sys.modules[__name__])
    del mod

import pkg_resources

for entrypoint in pkg_resources.iter_entry_points(group='janitoo.models'):
    logger.info("Extend models with %s", entrypoint)
    plugin = entrypoint.load()
    plugin( sys.modules[__name__] )
