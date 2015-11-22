"""Initial data

Revision ID: 33b95995b188
Revises: 1266567cc97f
Create Date: 2015-11-22 21:53:11.317987

"""

# revision identifiers, used by Alembic.
revision = '33b95995b188'
down_revision = '1266567cc97f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date, PickleType, Text, Boolean

def upgrade():
    core_groups = table('core_groups',
        column('name', String),
        column('description', Text),
        column('admin', Boolean),
        column('power', Boolean),
        column('user', Boolean),
        column('banned', Boolean),
        column('guest', Boolean),
        column('editpost', Boolean),
        column('deletepost', Boolean),
        column('deletetopic', Boolean),
        column('posttopic', Boolean),
        column('postreply', Boolean),
        column('mod_edituser', Boolean),
        column('mod_banuser', Boolean),
    )
    op.bulk_insert(core_groups,
        [
            {'name':'Administrator',
                'description': 'The Administrator Group',
                'admin': True,
                'power': False,
                'user': False,
                'banned': False,
                'guest': False,
                'editpost': True,
                'deletepost': True,
                'deletetopic': True,
                'posttopic': True,
                'postreply': True,
                'mod_edituser': True,
                'mod_banuser': True,
            },
            {'name':'Power',
                'description': 'The User with Power Group',
                'admin': False,
                'power': True,
                'user': False,
                'banned': False,
                'guest': False,
                'editpost': True,
                'deletepost': True,
                'deletetopic': True,
                'posttopic': True,
                'postreply': True,
                'mod_edituser': True,
                'mod_banuser': True,
            },
            {'name':'User',
                'description': 'The User Group',
                'admin': False,
                'power': False,
                'user': True,
                'banned': False,
                'guest': False,
                'editpost': False,
                'deletepost': False,
                'deletetopic': False,
                'posttopic': True,
                'postreply': True,
                'mod_edituser': False,
                'mod_banuser': False,
            },
            {'name':'Banned',
                'description': 'The Banned Group',
                'admin': False,
                'power': False,
                'user': False,
                'banned': True,
                'guest': False,
                'editpost': False,
                'deletepost': False,
                'deletetopic': False,
                'posttopic': False,
                'postreply': False,
                'mod_edituser': False,
                'mod_banuser': False,
            },
            {'name':'Guest',
                'description': 'The Guest Group',
                'admin': False,
                'power': False,
                'user': False,
                'banned': False,
                'guest': True,
                'editpost': False,
                'deletepost': False,
                'deletetopic': False,
                'posttopic': False,
                'postreply': False,
                'mod_edituser': False,
                'mod_banuser': False,
            }
        ]
    )

    core_settings_group = table('core_settings_group',
        column('key', String),
        column('name', String),
        column('description', Text),
    )
    op.bulk_insert(core_settings_group,
        [
            {'key':'general', 'name':'General Settings', 'description':'General Settings for janitoo.'},
            {'key':'appearance', 'name':'Appearance Settings', 'description':'Change the theme and language for your forum.'},
        ]
    )

    core_settings = table('core_settings',
        column('key', String),
        column('name', String),
        column('description', Text),
        column('value', PickleType),
        column('value_type', String),
        column('settinggroup', String),
        column('extra', PickleType)
    )
    op.bulk_insert(core_settings,
        [
            {'key':'project_title', 'name':'Project title', 'description':'The title of the project.','value_type':'string', 'value':'Janitoo', 'extra':None, 'settinggroup':"general"},
            {'key':'project_subtitle', 'name':'Project subtitle', 'description':'A short description of the project.','value_type':'string', 'value':'Janitoo', 'extra':None, 'settinggroup':"general"},
            {'key':'posts_per_page', 'name':'Project title', 'description':'Number of posts displayed per page.','value_type':'integer', 'value':10, 'extra':{'min': 5}, 'settinggroup':"general"},
            {'key':'topics_per_page', 'name':'Project title', 'description':'Number of topics displayed per page.','value_type':'integer', 'value':10, 'extra':{'min': 5}, 'settinggroup':"general"},
            {'key':'users_per_page', 'name':'Project title', 'description':'Number of users displayed per page.','value_type':'integer', 'value':10, 'extra':{'min': 5}, 'settinggroup':"general"},

            {'key':'default_theme', 'name':'Default Theme', 'description':'Change the default theme for your forum.','value_type':'select', 'value':'admin', 'extra':{'choices': [('admin','admin'),('bootstrap3','bootstrap3'),('bootstrap2','bootstrap2')]}, 'settinggroup':"appearance"},
            {'key':'default_language', 'name':'Default Language', 'description':'Change the default language for your forum.','value_type':'string', 'value':'en', 'extra':{'choices': [('en','English')]}, 'settinggroup':"appearance"},
        ]
    )


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###
