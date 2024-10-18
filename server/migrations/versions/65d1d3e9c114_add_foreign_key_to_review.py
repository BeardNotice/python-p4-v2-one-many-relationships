"""add foreign key to Review

Revision ID: 65d1d3e9c114
Revises: 8383a9b7785d
Create Date: 2024-10-18 12:11:43.755771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65d1d3e9c114'
down_revision = '8383a9b7785d'
branch_labels = None
depends_on = None


def upgrade():
    # Commands to add a new column and foreign key to the existing table
    with op.batch_alter_table("reviews") as batch_op:
        batch_op.add_column(sa.Column('employee_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_reviews_employee_id_employees', 
            'employees', 
            ['employee_id'], 
            ['id']
        )

def downgrade():
    # Commands to remove the foreign key and column
    with op.batch_alter_table("reviews") as batch_op:
        batch_op.drop_constraint('fk_reviews_employee_id_employees', type_='foreignkey')
        batch_op.drop_column('employee_id')
