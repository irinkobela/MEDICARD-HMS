"""Initial migration with User, Patient, Admission, Result, Imaging, Consult, Order models

Revision ID: 80f689f3fac0
Revises: 
Create Date: 2025-04-13 03:41:36.312218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80f689f3fac0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('admission_date', sa.DateTime(), nullable=False),
    sa.Column('discharge_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('consult',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admission_id', sa.Integer(), nullable=False),
    sa.Column('consultant_name', sa.String(length=100), nullable=False),
    sa.Column('consult_date', sa.DateTime(), nullable=False),
    sa.Column('consult_notes', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['admission_id'], ['admission.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('imaging',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admission_id', sa.Integer(), nullable=False),
    sa.Column('image_type', sa.String(length=100), nullable=False),
    sa.Column('image_date', sa.DateTime(), nullable=False),
    sa.Column('image_file', sa.LargeBinary(), nullable=True),
    sa.Column('image_report', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['admission_id'], ['admission.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admission_id', sa.Integer(), nullable=False),
    sa.Column('order_type', sa.String(length=50), nullable=False),
    sa.Column('order_name', sa.String(length=100), nullable=False),
    sa.Column('order_details', sa.Text(), nullable=True),
    sa.Column('order_date', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['admission_id'], ['admission.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admission_id', sa.Integer(), nullable=False),
    sa.Column('test_name', sa.String(length=100), nullable=False),
    sa.Column('result_value', sa.String(length=100), nullable=False),
    sa.Column('result_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['admission_id'], ['admission.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('result')
    op.drop_table('order')
    op.drop_table('imaging')
    op.drop_table('consult')
    op.drop_table('admission')
    # ### end Alembic commands ###
