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
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

import logging
logger = logging.getLogger(__name__)
import os
import pkg_resources
import tempfile
import shutil
import random
import string

import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from alembic.script import ScriptDirectory
from alembic.config import Config as alConfig
from alembic import command as alcommand
from alembic.migration import MigrationContext

from janitoo.options import JNTOptions

def janitoo_config(url=u'sqlite:////tmp/janitoo_db.sqlite',pkg_name='janitoo_db',  conf_file=None):
    """Retrive a global config by collecting entry_points
    DEPRECATED
    """
    config = Config(url=url, conf_file=conf_file)
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
    def __init__(self, url=u'sqlite:////tmp/janitoo_db.sqlite', pkg_name='janitoo_db', ep_name='janitoo', conf_file=None, **kwargs):
        """
        """
        self.pkg_name = pkg_name
        self.ep_name = ep_name
        if conf_file is None:
            src = os.path.join(pkg_resources.resource_filename(pkg_resources.Requirement.parse(self.pkg_name), 'config'), u'alembic_template.conf')
        else:
            src = conf_file
            options = JNTOptions({'conf_file':conf_file})
            options.load()
            alembic = options.get_options('database')
            url = alembic['sqlalchemy.url']
        file_ = os.path.join(tempfile.gettempdir(), u'jntal_%s.conf')%(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(26)))
        shutil.copyfile(src, file_)
        alConfig.__init__(self, file_=file_, ini_section='database', **kwargs)
        config_path = pkg_resources.resource_filename(pkg_resources.Requirement.parse(self.pkg_name), 'config')
        self.set_main_option("script_location", os.path.join(config_path, 'alembic'))
        self.set_main_option("sqlalchemy.url", url)
        version_locations = u"%s/alembic/versions %s/models/%s"%(config_path, config_path, self.ep_name)
        for entrypoint in pkg_resources.iter_entry_points(group='janitoo.models'):
            pkg = entrypoint.module_name.split('.')[0]
            config_path = pkg_resources.resource_filename(pkg_resources.Requirement.parse(pkg), 'config')
            version_locations +=  u" %s/models/%s"%(config_path, entrypoint.name)
        self.set_main_option("version_locations", version_locations)

    @property
    def url(self):
        """Return the db url"""
        return self.get_main_option("sqlalchemy.url", None)

    def __del__(self):
        """Remove config file when deleting object
        """
        try:
            os.unlink(self.config_file_name)
        except Exception:
            pass

    def initdb(self):
        """Initialise the database to heads
        """
        self.upgrade(revision='heads')

    def upgrade(self, revision='heads'):
        """Upgrade the database
        """
        alcommand.upgrade(self, revision)

    def downgrade(self, revision='base'):
        """Downgrade the database
        """
        alcommand.downgrade(self, revision)

    def versiondb(self):
        """Downgrade the database
        """
        engine = create_engine(self.url)
        conn = engine.connect()
        context = MigrationContext.configure(conn)
        return context.get_current_heads()

    def checkdb(self):
        """Check the database is up to date
        """
        heads = self.heads()
        versions = self.versiondb()
        if len(heads) != len(versions):
            return False
        for head in heads:
            if head.revision not in versions:
                return False
        return True

    def heads(self,verbose=False):
        """Get heads of the migration scripts
        """
        script = ScriptDirectory.from_config(self)
        return script.get_revisions("heads")
