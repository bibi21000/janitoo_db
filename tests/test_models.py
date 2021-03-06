# -*- coding: utf-8 -*-

"""Unittests for models.
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
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

import warnings
warnings.filterwarnings("ignore")

import sys, os
import time, datetime
import unittest
import threading
import logging
from pkg_resources import iter_entry_points

from sqlalchemy.orm import sessionmaker, scoped_session

from janitoo_nosetests import JNTTBase, DBCONFS
from janitoo_nosetests.models import JNTTModels, JNTTModelsCommon, jntt_models

from janitoo.options import JNTOptions
from janitoo_db.base import Base, create_db_engine

import janitoo_db.models as jntmodels

class ModelsCommon(JNTTModelsCommon):
    """Test the models
    """

    def test_101_user(self):
        self.create_all()
        group = jntmodels.Group(name="test_group")
        user = jntmodels.User(username="test_user", email="test@gmail.com", _password="test", primary_group=group)
        self.dbsession.add_all([group, user])
        self.dbsession.commit()

    def test_102_user_delete_cascade(self):
        self.skipSqliteTest()
        self.create_all()
        count = self.dbsession.query(jntmodels.groups_users).count()
        pgroup = jntmodels.Group(name="primary_group")
        sgroup1 = jntmodels.Group(name="secondary_group_1")
        sgroup2 = jntmodels.Group(name="secondary_group_2")
        user = jntmodels.User(username="test_user", email="test@gmail.com", _password="test", primary_group=pgroup, secondary_groups=[sgroup1,sgroup2])
        self.dbsession.add_all([pgroup, sgroup1, sgroup1, user])
        self.dbsession.commit()
        self.assertEqual(count+2, self.dbsession.query(jntmodels.groups_users).count())
        self.dbsession.delete(user)
        self.dbsession.commit()
        self.assertEqual(count, self.dbsession.query(jntmodels.groups_users).count())

class TestModels(JNTTModels, ModelsCommon):
    """Test the models
    """
    models_conf = "tests/data/janitoo_db.conf"

JNTTBase.skipCITest()
jntt_models(__name__, ModelsCommon, prefix='Db', dbs=[DBCONFS[2]])
