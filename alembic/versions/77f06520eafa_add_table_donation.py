"""Add table donation

Revision ID: 77f06520eafa
Revises: 401b592a7916
Create Date: 2023-07-08 10:18:25.370464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77f06520eafa'
down_revision = '401b592a7916'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('donation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('full_amount', sa.Integer(), nullable=True),
    sa.Column('invested_amount', sa.Integer(), nullable=True),
    sa.Column('fully_invested', sa.Boolean(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('close_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_donation_create_date'), 'donation', ['create_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_donation_create_date'), table_name='donation')
    op.drop_table('donation')
    # ### end Alembic commands ###