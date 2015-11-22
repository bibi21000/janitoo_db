"""Initial import

Revision ID: 1266567cc97f
Revises: 3b5854d25914
Create Date: 2015-11-17 00:01:03.441237

"""

# revision identifiers, used by Alembic.
revision = '1266567cc97f'
down_revision = '3b5854d25914'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('core_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.Column('power', sa.Boolean(), nullable=False),
    sa.Column('user', sa.Boolean(), nullable=False),
    sa.Column('guest', sa.Boolean(), nullable=False),
    sa.Column('banned', sa.Boolean(), nullable=False),
    sa.Column('mod_edituser', sa.Boolean(), nullable=False),
    sa.Column('mod_banuser', sa.Boolean(), nullable=False),
    sa.Column('editpost', sa.Boolean(), nullable=False),
    sa.Column('deletepost', sa.Boolean(), nullable=False),
    sa.Column('deletetopic', sa.Boolean(), nullable=False),
    sa.Column('posttopic', sa.Boolean(), nullable=False),
    sa.Column('postreply', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('core_settings',
    sa.Column('key', sa.String(length=255), nullable=False),
    sa.Column('value', sa.PickleType(), nullable=False),
    sa.Column('settinggroup', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('value_type', sa.String(length=20), nullable=False),
    sa.Column('extra', sa.PickleType(), nullable=True),
    sa.ForeignKeyConstraint(['settinggroup'], ['core_settings_group.key'], name='fk_settings_group', use_alter=True),
    sa.PrimaryKeyConstraint('key')
    )
    op.create_table('core_settings_group',
    sa.Column('key', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('key')
    )
    op.create_table('core_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('date_joined', sa.DateTime(), nullable=True),
    sa.Column('lastseen', sa.DateTime(), nullable=True),
    sa.Column('birthday', sa.DateTime(), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=True),
    sa.Column('website', sa.String(length=200), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('signature', sa.Text(), nullable=True),
    sa.Column('avatar', sa.String(length=200), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('theme', sa.String(length=15), nullable=True),
    sa.Column('language', sa.String(length=15), nullable=True),
    sa.Column('primary_group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['primary_group_id'], ['core_groups.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('core_groups_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['core_groups.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['core_users.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('core_groups_users')
    op.drop_table('core_users')
    op.drop_table('core_settings_group')
    op.drop_table('core_settings')
    op.drop_table('core_groups')
    ### end Alembic commands ###
