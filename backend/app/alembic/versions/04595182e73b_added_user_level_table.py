"""Added user level table

Revision ID: 04595182e73b
Revises: 6f19ff3ddfa0
Create Date: 2025-01-26 10:15:42.273349

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '04595182e73b'
down_revision = '6f19ff3ddfa0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee_levels',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('employee_id', sa.Uuid(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('level_start_date', sa.DateTime(), nullable=False),
    sa.Column('level_end_date', sa.DateTime(), nullable=True),
    sa.Column('xp', sa.Integer(), nullable=False),
    sa.Column('xp_multiplier', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('employee_level_id', sa.Uuid(), nullable=False))
    op.create_foreign_key(None, 'user', 'employee_levels', ['employee_level_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'employee_level_id')
    op.drop_table('employee_levels')
    # ### end Alembic commands ###
