# -*- coding: utf-8 -*-
"""
    janitoo_manager.utils.database
    ~~~~~~~~~~~~~~~~~~~~~~

    Some database helpers such as a CRUD mixin.

    :copyright: (c) 2015 by the janitoo_manager Team.
    :license: BSD, see LICENSE for more details.
"""
import logging
logger = logging.getLogger( "janitoo.db" )
from sqlalchemy.orm import class_mapper

class CRUDMixin(object):
    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

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
