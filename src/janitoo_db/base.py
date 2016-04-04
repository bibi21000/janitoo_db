# -*- coding: utf-8 -*-
"""
    janitoo_db.base
    ~~~~~~~~~~~~~~~
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
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def create_db_engine(options):
    """Create the sql alchemy engine
    """
    alembic = options.get_options('database')
    return sqlalchemy.engine_from_config(alembic, prefix='sqlalchemy.')

#DEprecated
def check_version_db(options, extension="janitoo"):
    """
    """
    logger.debug(u'[%s] - Start checking db version for extension %s', self.__class__.__name__, extension)
    self._create_db_engine()
    #We must retrieve tables from database to ensure it exist
    if migrate == False or (migrate is None and self.dbauto_migrate == False):
        #We should improve this by checking version in db and and alembic.
        if self.dbengine.dialect.has_table(self.dbengine.connect(), "dhcpd_lease") == False or self.dbengine.dialect.has_table(self.dbengine.connect(), "dhcpd_lease_param") == False:
            raise JanitooException(u"Cant't find tables in database and auto_update is not enable. Please create database and tables by hand.")
        logger.debug(u'[%s] - Finishing quick check of database', self.__class__.__name__)
        return
    config = alConfig(file_=self.options.data['conf_file'], ini_section='database')
    config.set_main_option("script_location", os.path.join(self._get_egg_path(), "alembic"))
    alcommand.upgrade(config, "head")
    logger.debug(u'[%s] - Finishing full check of database', self.__class__.__name__)

#DEprecated
def check_db(options, migrate=None):
    """Check the db version and update if needed and allowed
    migrate == None : use auto_migrate from conf_file
    """
    logger.debug(u'[%s] - Start checking database', self.__class__.__name__)
    self._create_db_engine()
    #We must retrieve tables from database to ensure it exist
    if migrate == False or (migrate is None and self.dbauto_migrate == False):
        #We should improve this by checking version in db and and alembic.
        if self.dbengine.dialect.has_table(self.dbengine.connect(), "dhcpd_lease") == False or self.dbengine.dialect.has_table(self.dbengine.connect(), "dhcpd_lease_param") == False:
            raise JanitooException(u"Cant't find tables in database and auto_update is not enable. Please create database and tables by hand.")
        logger.debugu('[%s] - Finishing quick check of database', self.__class__.__name__)
        return
    config = alConfig(file_=self.options.data['conf_file'], ini_section='database')
    config.set_main_option("script_location", os.path.join(self._get_egg_path(), "alembic"))
    alcommand.upgrade(config, "head")
    logger.debug(u'[%s] - Finishing full check of database', self.__class__.__name__)

#DEprecated
def create_session():
    """Create a scoped session
    """
    sess = None
    if self.dbmaker is not None:
        sess = scoped_session(self.dbmaker)
    return sess

#DEprecated
def start_db():
    """Open the db connection
    """
    self._create_db_engine()
    # Construct a sessionmaker object
    self.dbmaker = sessionmaker()
    # Bind the sessionmaker to engine
    self.dbmaker.configure(bind=self.dbengine)
    self.dbsession = self.create_session()
