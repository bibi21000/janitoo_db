# -*- coding: utf-8 -*-
"""
    janitoo_db.migrate
    ~~~~~~~~~~~~~~~~~~

    http://alembic.readthedocs.org/en/latest/branches.html

    Each extension has it own labelled branch (the name of the entry_poiunt)

    We build a temporary config grouping all version locations


"""

_license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014 Sébastien GALLET aka bibi21000"

import logging
logger = logging.getLogger( u"janitoo.db" )
import os
import pkg_resources
import tempfile
import shutil
import random
import string

import sqlalchemy

from alembic.config import Config as alConfig
from alembic.script import ScriptDirectory as alScriptDirectory
from alembic import command as alcommand

def janitoo_config(url=u'sqlite:////tmp/janitoo_db.sqlite',pkg_name='janitoo_db',  conf_file=u'alembic_template.conf'):
    """Retrive a global config by collecting entry_points
    todo : take care of dependencies to order config by dependances
    """
    config = Config(url=url, conf_file=conf_file)
    version_locations = config.get_main_option("version_locations")
    for entrypoint in pkg_resources.iter_entry_points(group='janitoo.models'):
        pkg_name = entrypoint.module_name.split('.')[0]
        config_path = pkg_resources.resource_filename(pkg_resources.Requirement.parse(pkg_name), 'config')
        version_locations +=  u" %s/models/%s"%(config_path, entrypoint.name)
    config.set_main_option("version_locations", version_locations)
    return config

def collect_configs(url='sqlite:////tmp/janitoo_db.sqlite'):
    """Collect all configs
    todo : take care of dependencies to order config by dependances
    """
    ret = []
    config = Config(url=url)
    ret.append(config)
    for entrypoint in pkg_resources.iter_entry_points(group='janitoo.models'):
        pkg_name = entrypoint.module_name.split('.')[0]
        config = Config(url=url, pkg_name=pkg_name, ep_name=entrypoint.name)
        ret.append(config)
    return ret

class Config(alConfig):
    """Generate an alembic config for janitoo extension
    """
    def __init__(self, url=u'sqlite:////tmp/janitoo_db.sqlite', pkg_name='janitoo_db', ep_name='janitoo', conf_file=u'alembic_template.conf', **kwargs):
        """
        """
        file_ = os.path.join(tempfile.gettempdir(), u'jntal_%s.conf')%(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(26)))
        src = os.path.join(pkg_resources.resource_filename(pkg_resources.Requirement.parse(pkg_name), 'config'), conf_file)
        shutil.copyfile(src, file_)
        alConfig.__init__(self, file_=file_, ini_section='database', **kwargs)
        self.pkg_name = pkg_name
        self.ep_name = ep_name
        config_path = pkg_resources.resource_filename(pkg_resources.Requirement.parse(pkg_name), 'config')
        self.set_main_option("script_location", os.path.join(config_path, 'alembic'))
        self.set_main_option("sqlalchemy.url", url)
        self.set_main_option("version_locations", "u%s/alembic/versions %s/models/%s"%(config_path, config_path, ep_name))

    def __del__(self):
        """
        """
        try:
            os.unlink(self.config_file_name)
        except:
            pass
