# -*- coding: utf-8 -*-
"""
    janitoo_db.models.utils
    ~~~~~~~~~~~~~~~~~~~~~~~

    This module contains all utild related models.

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
__copyright__ = "Copyright © 2014-2015 Sébastien GALLET aka bibi21000"
import logging
logger = logging.getLogger(__name__)

import sys
import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref

from janitoo_db.helpers import CRUDMixin
from janitoo_db.base import Base

def extend( jntmodel ):

    class SettingGroup(Base, CRUDMixin):
        __tablename__ = "core_settings_group"

        key = sa.Column(sa.String(255), primary_key=True)
        name = sa.Column(sa.String(255), nullable=False)
        description = sa.Column(sa.Text, nullable=False)
        settings = relationship("Setting", lazy="dynamic", backref="group",
                                   cascade="all, delete-orphan")
    jntmodel.SettingGroup = SettingGroup

    # hack to get class pickable
    setattr(sys.modules[__name__], 'SettingGroup', SettingGroup)

    class Setting(Base, CRUDMixin):
        __tablename__ = "core_settings"

        key = sa.Column(sa.String(255), primary_key=True)
        value = sa.Column(sa.PickleType, nullable=False)
        #~ settinggroup = sa.Column(sa.String(255),
                                  #~ sa.ForeignKey('core_settings_group.key',
                                                #~ use_alter=True,
                                                #~ name="fk_settings_group"),
        settinggroup_key = sa.Column(sa.String(255), sa.ForeignKey('core_settings_group.key'),
                                     nullable=False)

        settinggroup = relationship('SettingGroup', lazy="joined",
                                        backref="core_settings_group", uselist=False,
                                        foreign_keys=[settinggroup_key])

        # The name (displayed in the form)
        name = sa.Column(sa.String(200), nullable=False)

        # The description (displayed in the form)
        description = sa.Column(sa.Text, nullable=False)

        # Available types: string, integer, float, boolean, select, selectmultiple
        value_type = sa.Column(sa.String(20), nullable=False)

        # Extra attributes like, validation things (min, max length...)
        # For Select*Fields required: choices
        extra = sa.Column(sa.PickleType)

        @classmethod
        def get_all(cls):
            return cls.query.all()

        @classmethod
        def get_settings(cls, from_group=None):
            """This will return all settings with the key as the key for the dict
            and the values are packed again in a dict which contains
            the remaining attributes.

            :param from_group: Optionally - Returns only the settings from a group.
            """
            result = None
            if from_group is not None:
                result = from_group.settings
            else:
                result = cls.query.all()
            settings = {}
            for setting in result:
                settings[setting.key] = {
                    'name': setting.name,
                    'description': setting.description,
                    'value': setting.value,
                    'value_type': setting.value_type,
                    'extra': setting.extra
                }
            return settings

        @classmethod
        def as_dict(cls, from_group=None, upper=True):
            """Returns all settings as a dict. This method is cached. If you want
            to invalidate the cache, simply execute ``self.invalidate_cache()``.

            :param from_group: Returns only the settings from the group as a dict.
            :param upper: If upper is ``True``, the key will use upper-case
                          letters. Defaults to ``False``.
            """

            settings = {}
            result = None
            if from_group is not None:
                result = SettingGroup.query.filter_by(key=from_group).\
                    first()
                if result:
                    result = result.settings
                else:
                    result = []
            else:
                #~ print(Setting.query)
                result = cls.query.all()
            #~ print result
            for setting in result:
                if upper:
                    setting_key = setting.key.upper()
                else:
                    setting_key = setting.key

                settings[setting_key] = setting.value
            return settings

    jntmodel.Setting = Setting

    # hack to get class pickable
    setattr(sys.modules[__name__], 'Setting', Setting)
