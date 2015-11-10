# -*- coding: utf-8 -*-
"""
    janitoo_db.mdels.user
    ~~~~~~~~~~~~~~~~~~~~~

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
__copyright__ = "Copyright © 2013-2014 Sébastien GALLET aka bibi21000"

import logging
logger = logging.getLogger( "janitoo_db" )
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref, synonym
from janitoo_db.helpers import CRUDMixin
from janitoo_db.base import Base
from janitoo_db.security import generate_password_hash, check_password_hash

groups_users = sa.Table(
    'core_groups_users',
    Base.metadata,
    sa.Column('user_id', sa.Integer(), sa.ForeignKey('core_users.id')),
    sa.Column('group_id', sa.Integer(), sa.ForeignKey('core_groups.id')))


class Group(Base, CRUDMixin):
    __tablename__ = "core_groups"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), unique=True, nullable=False)
    description = sa.Column(sa.Text)

    # Group types
    admin = sa.Column(sa.Boolean, default=False, nullable=False)
    power = sa.Column(sa.Boolean, default=False, nullable=False)
    user = sa.Column(sa.Boolean, default=False, nullable=False)
    guest = sa.Column(sa.Boolean, default=False, nullable=False)
    banned = sa.Column(sa.Boolean, default=False, nullable=False)

    # Moderator permissions (only available when the user a moderator)
    mod_edituser = sa.Column(sa.Boolean, default=False, nullable=False)
    mod_banuser = sa.Column(sa.Boolean, default=False, nullable=False)

    # User permissions
    editpost = sa.Column(sa.Boolean, default=True, nullable=False)
    deletepost = sa.Column(sa.Boolean, default=False, nullable=False)
    deletetopic = sa.Column(sa.Boolean, default=False, nullable=False)
    posttopic = sa.Column(sa.Boolean, default=True, nullable=False)
    postreply = sa.Column(sa.Boolean, default=True, nullable=False)

    # Methods
    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    @classmethod
    def selectable_groups_choices(cls):
        return Group.query.order_by(Group.name.asc()).with_entities(
            Group.id, Group.name
        ).all()

    @classmethod
    def get_guest_group(cls):
        return Group.query.filter(cls.guest == True).first()


class User(Base, CRUDMixin):
    __tablename__ = "core_users"

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(200), unique=True, nullable=False)
    email = sa.Column(sa.String(200), unique=True, nullable=False)
    _password = sa.Column('password', sa.String(120), nullable=False)
    date_joined = sa.Column(sa.DateTime, default=datetime.utcnow())
    lastseen = sa.Column(sa.DateTime, default=datetime.utcnow())
    birthday = sa.Column(sa.DateTime)
    gender = sa.Column(sa.String(10))
    website = sa.Column(sa.String(200))
    location = sa.Column(sa.String(100))
    signature = sa.Column(sa.Text)
    avatar = sa.Column(sa.String(200))
    notes = sa.Column(sa.Text)

    theme = sa.Column(sa.String(15))
    language = sa.Column(sa.String(15), default="en")

    primary_group_id = sa.Column(sa.Integer, sa.ForeignKey('core_groups.id'),
                                 nullable=False)

    primary_group = relationship('Group', lazy="joined",
                                    backref="user_group", uselist=False,
                                    foreign_keys=[primary_group_id])

    secondary_groups = \
        relationship('Group',
                        secondary=groups_users,
                        primaryjoin=(groups_users.c.user_id == id),
                        backref=backref('users', lazy='dynamic'),
                        lazy='dynamic')

    @property
    def permissions(self):
        """Returns the permissions for the user"""
        return self.get_permissions()

    @property
    def groups(self):
        """Returns user groups"""
        return self.get_groups()

    @property
    def days_registered(self):
        """Returns the amount of days the user is registered."""
        days_registered = (datetime.utcnow() - self.date_joined).days
        if not days_registered:
            return 1
        return days_registered

    # Methods
    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.username)

    def _get_password(self):
        """Returns the hashed password"""
        return self._password

    def _set_password(self, password):
        """Generates a password hash for the provided password"""
        self._password = generate_password_hash(password)

    # Hide password encryption by exposing password field only.
    password = synonym('_password',
                          descriptor=property(_get_password,
                                              _set_password))

    def check_password(self, password):
        """Check passwords. If passwords match it returns true, else false"""

        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, login, password):
        """A classmethod for authenticating users
        It returns true if the user exists and has entered a correct password

        :param login: This can be either a username or a email address.

        :param password: The password that is connected to username and email.
        """

        user = cls.query.filter(sa.or_(User.username == login,
                                       User.email == login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    def _make_token(self, data, timeout):
        s = Serializer(current_app.config['SECRET_KEY'], timeout)
        return s.dumps(data)

    def _verify_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        data = None
        expired, invalid = False, False
        try:
            data = s.loads(token)
        except SignatureExpired:
            expired = True
        except Exception:
            invalid = True
        return expired, invalid, data

    def make_reset_token(self, expiration=3600):
        """Creates a reset token. The duration can be configured through the
        expiration parameter.

        :param expiration: The time in seconds how long the token is valid.
        """
        return self._make_token({'id': self.id, 'op': 'reset'}, expiration)

    def verify_reset_token(self, token):
        """Verifies a reset token. It returns three boolean values based on
        the state of the token (expired, invalid, data)

        :param token: The reset token that should be checked.
        """

        expired, invalid, data = self._verify_token(token)
        if data and data.get('id') == self.id and data.get('op') == 'reset':
            data = True
        else:
            data = False
        return expired, invalid, data

    def add_to_group(self, group):
        """Adds the user to the `group` if he isn't in it.

        :param group: The group which should be added to the user.
        """

        if not self.in_group(group):
            self.secondary_groups.append(group)
            return self

    def remove_from_group(self, group):
        """Removes the user from the `group` if he is in it.

        :param group: The group which should be removed from the user.
        """

        if self.in_group(group):
            self.secondary_groups.remove(group)
            return self

    def in_group(self, group):
        """Returns True if the user is in the specified group

        :param group: The group which should be checked.
        """

        return self.secondary_groups.filter(
            groups_users.c.group_id == group.id).count() > 0

    def get_groups(self):
        """Returns all the groups the user is in."""
        return [self.primary_group] + list(self.secondary_groups)

    def get_permissions(self, exclude=None):
        """Returns a dictionary with all the permissions the user has.

        :param exclude: a list with excluded permissions. default is None.
        """

        exclude = exclude or []
        exclude.extend(['id', 'name', 'description'])

        perms = {}
        groups = self.secondary_groups.all()
        groups.append(self.primary_group)
        for group in groups:
            for c in group.__table__.columns:
                # try if the permission already exists in the dictionary
                # and if the permission is true, set it to True
                try:
                    if not perms[c.name] and getattr(group, c.name):
                        perms[c.name] = True

                # if the permission doesn't exist in the dictionary
                # add it to the dictionary
                except KeyError:
                    # if the permission is in the exclude list,
                    # skip to the next permission
                    if c.name in exclude:
                        continue
                    perms[c.name] = getattr(group, c.name)
        return perms

    def ban(self):
        """Bans the user. Returns True upon success."""

        if not self.get_permissions()['banned']:
            banned_group = Group.query.filter(
                Group.banned == True
            ).first()

            self.primary_group_id = banned_group.id
            self.save()
            return True
        return False

    def unban(self):
        """Unbans the user. Returns True upon success."""

        if self.get_permissions()['banned']:
            member_group = Group.query.filter(
                Group.admin == False,
                Group.super_mod == False,
                Group.mod == False,
                Group.guest == False,
                Group.banned == False
            ).first()

            self.primary_group_id = member_group.id
            self.save()
            return True
        return False

    def save(self, db, groups=None):
        """Saves a user. If a list with groups is provided, it will add those
        to the secondary groups from the user.

        :param groups: A list with groups that should be added to the
                       secondary groups from user.
        """

        if groups is not None:
            # TODO: Only remove/add groups that are selected
            secondary_groups = self.secondary_groups.all()
            for group in secondary_groups:
                self.remove_from_group(group)
            sa.session.commit()

            for group in groups:
                # Do not add the primary group to the secondary groups
                if group.id == self.primary_group_id:
                    continue
                self.add_to_group(group)

        db.session.add(self)
        db.session.commit()
        return self

    def delete(self, db):
        """Deletes the User."""

        db.session.delete(self)
        db.session.commit()

        return self


class Guest():
    @property
    def permissions(self):
        return self.get_permissions()

    def get_permissions(self, exclude=None):
        """Returns a dictionary with all permissions the user has"""
        exclude = exclude or []
        exclude.extend(['id', 'name', 'description'])

        perms = {}
        # Get the Guest group
        group = Group.query.filter_by(guest=True).first()
        for c in group.__table__.columns:
            if c.name in exclude:
                continue
            perms[c.name] = getattr(group, c.name)
        return perms

