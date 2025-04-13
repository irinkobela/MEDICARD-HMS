"""Add indicator fields to Result, Imaging, Consult, Order

Revision ID: a6c46181862f
Revises: 02947fa2b623
Create Date: 2025-04-13 05:42:22.963637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6c46181862f'
down_revision = '02947fa2b623'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('consult', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assigned_physician_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('read_at', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_consult_assigned_physician_id'), ['assigned_physician_id'], unique=False)
        batch_op.create_foreign_key(None, 'user', ['assigned_physician_id'], ['id'])

    with op.batch_alter_table('imaging', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_critical', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('acknowledged_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('acknowledged_by_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['acknowledged_by_id'], ['id'])

    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('responsible_attending_id', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_order_responsible_attending_id'), ['responsible_attending_id'], unique=False)
        batch_op.create_foreign_key(None, 'user', ['responsible_attending_id'], ['id'])

    with op.batch_alter_table('result', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_critical', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('acknowledged_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('acknowledged_by_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['acknowledged_by_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('result', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('acknowledged_by_id')
        batch_op.drop_column('acknowledged_at')
        batch_op.drop_column('is_critical')

    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_order_responsible_attending_id'))
        batch_op.drop_column('responsible_attending_id')

    with op.batch_alter_table('imaging', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('acknowledged_by_id')
        batch_op.drop_column('acknowledged_at')
        batch_op.drop_column('is_critical')

    with op.batch_alter_table('consult', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_consult_assigned_physician_id'))
        batch_op.drop_column('read_at')
        batch_op.drop_column('status')
        batch_op.drop_column('assigned_physician_id')

    # ### end Alembic commands ###
