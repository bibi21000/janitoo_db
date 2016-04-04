# -*- coding: utf-8 -*-
"""
    janitoo_manager.utils.database
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Some database helpers such as a CRUD mixin.
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
from sqlalchemy.orm import class_mapper, Query
from datetime import datetime

class CRUDMixin(object):
    def __repr__(self):
        return u"<{}>".format(self.__class__.__name__)

    def save(self, db):
        """Saves the object to the database."""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self, db):
        """Delete the object from the database."""
        db.session.delete(self)
        db.session.commit()
        return self

def saobject_to_dict(obj, found=None):
    if found is None:
        found = set()
    mapper = class_mapper(obj.__class__)
    columns = [column.key for column in mapper.columns]
    get_key_value = lambda c: (c, getattr(obj, c).isoformat()) if isinstance(getattr(obj, c), datetime) else (c, getattr(obj, c))
    out = dict(map(get_key_value, columns))
    for name, relation in mapper.relationships.items():
        if relation not in found:
            found.add(relation)
            related_obj = getattr(obj, name)
            if related_obj is not None:
                if relation.uselist:
                    out[name] = [saobject_to_dict(child, found) for child in related_obj]
                else:
                    out[name] = saobject_to_dict(related_obj, found)
    return out
