from alembic import op
import sqlalchemy as sa


revision = '80d00e46bdc3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "station_tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("server_task_id", sa.Integer(), nullable=False, unique=True),
        sa.Column("product_name", sa.String(), nullable=False),
        sa.Column("gtin", sa.String(), nullable=False),
        sa.Column("quantity_in_box", sa.Integer(), nullable=False),
        sa.Column("quantity_in_pallet", sa.Integer(), nullable=False),
        sa.Column("planned_quantity", sa.Integer(), nullable=False),
        sa.Column("scenario_code", sa.Integer()),
        sa.Column("scenario_name", sa.String()),
        sa.Column("status", sa.String(), nullable=False, server_default="queued"),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("started_at", sa.DateTime()),
        sa.Column("finished_at", sa.DateTime()),
    )


def downgrade():
    op.drop_table("station_tasks")