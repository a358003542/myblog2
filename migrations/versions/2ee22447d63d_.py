"""empty message

Revision ID: 2ee22447d63d
Revises: 6497222f70ba
Create Date: 2019-01-25 13:28:37.515269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ee22447d63d'
down_revision = '6497222f70ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###