# -*- coding: utf-8 -*-

"""Unittests for DHCP Server.
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

import sys, os
import time, datetime
import unittest
import threading
import logging
import time
from pkg_resources import iter_entry_points

from janitoo_nosetests.dbserver import JNTTDBServer, JNTTDBServerCommon
from janitoo_nosetests.thread import JNTTThread, JNTTThreadCommon

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC
from janitoo.utils import JanitooNotImplemented, JanitooException
from janitoo.options import JNTOptions
from janitoo_db.server import JNTDBServer

class TestDbSerser(JNTTDBServer, JNTTDBServerCommon):
    """Test the server
    """
    loglevel = logging.DEBUG
    path = '/tmp/janitoo_test'
    broker_user = 'toto'
    broker_password = 'toto'
    server_class = JNTDBServer
    server_conf = "tests/data/janitoo_db_server.conf"

    def test_051_dbserver_auto_migrate(self):
        options = JNTOptions({'conf_file':self.server_conf})
        options.load()
        options.set_option('database','auto_migrate', False)
        with self.assertRaises(JanitooException):
            self.start()
            self.assertHeartbeatNode()
            self.stop()

    def test_052_dbserver_auto_migrate(self):
        options = JNTOptions({'conf_file':self.server_conf})
        options.load()
        options.set_option('database','auto_migrate', True)
        self.start()
        self.assertHeartbeatNode()
        self.stop()