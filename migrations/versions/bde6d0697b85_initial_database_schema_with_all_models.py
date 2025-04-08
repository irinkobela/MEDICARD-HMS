"""Initial database schema with all models

Revision ID: bde6d0697b85
Revises: 
Create Date: 2025-04-08 04:46:55.312801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bde6d0697b85'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('consults',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('assigned_physician_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.Column('read_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('imaging',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('is_critical', sa.Boolean(), nullable=True),
    sa.Column('acknowledged_at', sa.DateTime(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.Column('responsible_attending_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('is_critical', sa.Boolean(), nullable=True),
    sa.Column('acknowledged_at', sa.DateTime(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mrn', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('sex', sa.String(length=10), nullable=True),
    sa.Column('location_bed', sa.String(length=64), nullable=True),
    sa.Column('primary_diagnosis_summary', sa.String(length=256), nullable=True),
    sa.Column('code_status', sa.String(length=64), nullable=True),
    sa.Column('isolation_status', sa.String(length=64), nullable=True),
    sa.Column('attending_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['attending_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_patients_mrn'), ['mrn'], unique=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=80), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_patients_mrn'))

    op.drop_table('patients')
    op.drop_table('results')
    op.drop_table('orders')
    op.drop_table('imaging')
    op.drop_table('consults')
    # ### end Alembic commands ###
