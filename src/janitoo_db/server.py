# -*- coding: utf-8 -*-
"""The base server for Janitoo

 - we must add a method to reload a thread (a key from entry point) : install new thread, update a thread

"""

__license__ = """
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
__copyright__ = "Copyright © 2013-2014-2015 Sébastien GALLET aka bibi21000"

# Set default logging handler to avoid "No handler found" warnings.
import logging
logger = logging.getLogger(__name__)
import os, sys
import threading
import signal
import time
from logging.config import fileConfig as logging_fileConfig
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from alembic.config import Config as alConfig
from alembic import command as alcommand
from pkg_resources import iter_entry_points
from janitoo.utils import JanitooNotImplemented, JanitooException
from janitoo.options import JNTOptions, string_to_bool
from janitoo.server import JNTServer
from janitoo_db.base import Base, create_db_engine
import janitoo_db.models as jntmodel
from janitoo_db.migrate import Config as alConfig, collect_configs

class JNTDBServer(JNTServer):
    """The Janitoo Server with a db connexion

    To migrate by hand :

        cd src-*/config
        alembic --config jnt_xxxxx.conf --name database upgrade head
        alembic --config jnt_xxxxx.conf --name database revision -m "Add a column"

    """
    def __init__(self, options):
        """Init the server. Must be called at the begin of the children class.
        """
        JNTServer.__init__(self, options)
        self.dbengine = None
        self.dbmaker = None
        self.dbsession = None
        self.dbauto_migrate = None
        self.check_db()

    def _create_db_engine(self):
        """Create the sql alchemy engine
        """
        logger.debug(u'[%s] - Create db engine', self.__class__.__name__)
        #~ self.stop_db()
        #print self.options
        if self.dbengine is not None:
            return True
        alembic = self.options.get_options('database')
        self.dbauto_migrate = string_to_bool(alembic['auto_migrate']) if 'auto_migrate' in alembic else None
        self.dbengine = create_db_engine(self.options)

    def check_db(self, migrate=None):
        """Check the db version and update if needed and allowed
        migrate == None : use auto_migrate from conf_file
        """
        logger.debug(u'[%s] - Start checking database', self.__class__.__name__)
        self._create_db_engine()
        alembic = self.options.get_options('database')
        config = alConfig(url=alembic['sqlalchemy.url'])
        if migrate == False or (migrate is None and self.dbauto_migrate == False):
            if not config.checkdb():
                raise JanitooException(u"Database is not up to date and auto_migrate is not enable. Please update your database by hand.")
            logger.debug(u'[%s] - Finishing quick check of database', self.__class__.__name__)
            return
        config.initdb()
        logger.debug(u'[%s] - Finishing full check/upgrade database', self.__class__.__name__)

    def create_session(self):
        """Create a scoped session
        """
        sess = None
        if self.dbmaker is not None:
            sess = scoped_session(self.dbmaker)
        return sess

    def start_db(self):
        """Open the db connection
        """
        self._create_db_engine()
        # Construct a sessionmaker object
        self.dbmaker = sessionmaker()
        # Bind the sessionmaker to engine
        self.dbmaker.configure(bind=self.dbengine)
        self.dbsession = self.create_session()

    def stop_db(self):
        """Close the db connection
        """
        if self.dbsession is not None:
            self.dbsession.rollback()
            self.dbsession.close()
            self.dbsession = None
        if self.dbmaker is not None:
            self.dbmaker.close_all()
            self.dbmaker = None
        if self.dbengine is not None:
            self.dbengine.dispose()
            self.dbengine = None

    def start(self):
        """Start the server. Must be called at the end of the children class.
        """
        self.start_db()
        JNTServer.start(self)

    def stop(self):
        """Stop the server the server. Must be called at end of the children class
        """
        self.stop_db()
        JNTServer.stop(self)

    def flush(self):
        """Flush the server's data to disk
        """
        JNTServer.flush(self)
