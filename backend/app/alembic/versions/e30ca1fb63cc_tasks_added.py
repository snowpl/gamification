"""Tasks added

Revision ID: e30ca1fb63cc
Revises: 04dd6d40ccf3
Create Date: 2025-01-18 18:14:23.077800

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'e30ca1fb63cc'
down_revision = '04dd6d40ccf3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employeetask',
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('requires_approval', sa.Boolean(), nullable=False),
    sa.Column('approved', sa.Boolean(), nullable=False),
    sa.Column('department_xp', sa.Integer(), nullable=False),
    sa.Column('skill_xp', sa.Integer(), nullable=False),
    sa.Column('company_xp', sa.Integer(), nullable=False),
    sa.Column('person_xp', sa.Integer(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('assigned_to_id', sa.Uuid(), nullable=False),
    sa.Column('approved_by_id', sa.Uuid(), nullable=False),
    sa.Column('department_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['approved_by_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['assigned_to_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employeetask')
    # ### end Alembic commands ###
