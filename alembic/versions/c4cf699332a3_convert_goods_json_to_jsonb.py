"""convert_goods_json_to_jsonb

Revision ID: c4cf699332a3
Revises: 111e55167960
Create Date: 2026-09-23 16:17:41.134525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c4cf699332a3'
down_revision: Union[str, Sequence[str], None] = '111e55167960'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Преобразуем VARCHAR(5000) в JSONB с использованием функции приведения типов в Postgres
    op.alter_column(
        'basket',
        'goods_json',
        existing_type=sa.VARCHAR(length=5000),
        type_=postgresql.JSONB(astext_type=sa.Text()),
        existing_nullable=True,
        postgresql_using='goods_json::jsonb'
    )


def downgrade() -> None:
    # Откат с JSONB обратно в VARCHAR(5000)
    op.alter_column(
        'basket',
        'goods_json',
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        type_=sa.VARCHAR(length=5000),
        existing_nullable=True,
        postgresql_using='goods_json::text'
    )
