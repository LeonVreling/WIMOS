"""resolutions

Revision ID: 1066445071d6
Revises: 770f6fbdee62
Create Date: 2020-06-26 22:30:54.112610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1066445071d6'
down_revision = '770f6fbdee62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resolution',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('observation', sa.String(length=512), nullable=False),
    sa.Column('consideration', sa.String(length=512), nullable=False),
    sa.Column('decision', sa.String(length=512), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('passed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vote',
    sa.Column('resolution_id', sa.Integer(), nullable=False),
    sa.Column('association', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['resolution_id'], ['resolution.id'], ),
    sa.PrimaryKeyConstraint('resolution_id', 'association')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vote')
    op.drop_table('resolution')
    # ### end Alembic commands ###
