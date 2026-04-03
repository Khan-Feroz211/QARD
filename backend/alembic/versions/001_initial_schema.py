"""Initial database schema migration: creates all QARD tables."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tenants",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("slug", sa.String(64), unique=True, nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("logo_url", sa.Text()),
        sa.Column("primary_color", sa.String(16)),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("plan", sa.Enum("free", "pro", "enterprise", name="tenant_plan"), default="free"),
        sa.Column("lms_api_url", sa.Text()),
        sa.Column("lms_api_key", sa.String(512)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("email", sa.String(256), unique=True, nullable=False),
        sa.Column("phone", sa.String(32)),
        sa.Column("hashed_password", sa.String(256), nullable=False),
        sa.Column("full_name", sa.String(256), nullable=False),
        sa.Column("student_id", sa.String(64)),
        sa.Column("profile_photo_url", sa.Text()),
        sa.Column("role", sa.Enum("student", "admin", "superadmin", name="user_role"), default="student"),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("is_verified", sa.Boolean(), default=False),
        sa.Column("plan", sa.Enum("free", "pro", name="user_plan"), default="free"),
        sa.Column("stripe_customer_id", sa.String(256)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "virtual_cards",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("card_number", sa.String(64), unique=True, nullable=False),
        sa.Column("qr_code_data", sa.Text()),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
        sa.Column("issued_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("last_used_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "academic_records",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("semester", sa.String(32), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("gpa", sa.Float()),
        sa.Column("cgpa", sa.Float()),
        sa.Column("program", sa.String(256)),
        sa.Column("department", sa.String(256)),
        sa.Column("status", sa.Enum("enrolled", "graduated", "on_leave", name="academic_status"), default="enrolled"),
        sa.Column("synced_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "course_results",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("academic_record_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("academic_records.id"), nullable=False),
        sa.Column("course_code", sa.String(32), nullable=False),
        sa.Column("course_name", sa.String(256), nullable=False),
        sa.Column("credits", sa.Integer(), nullable=False),
        sa.Column("grade", sa.String(8)),
        sa.Column("marks_obtained", sa.Float()),
        sa.Column("max_marks", sa.Float()),
    )

    op.create_table(
        "benefits",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("tenants.id"), nullable=True),
        sa.Column("title", sa.String(256), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("partner_name", sa.String(256), nullable=False),
        sa.Column("discount_percent", sa.Float(), nullable=False),
        sa.Column("category", sa.Enum("food", "transport", "books", "health", "entertainment", name="benefit_category"), nullable=False),
        sa.Column("logo_url", sa.Text()),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("valid_until", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "usage_events",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("card_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("virtual_cards.id"), nullable=False),
        sa.Column("merchant_name", sa.String(256)),
        sa.Column("location", sa.String(512)),
        sa.Column("amount_pkr", sa.Numeric(12, 2)),
        sa.Column("event_type", sa.Enum("scan", "login", "benefit_claimed", name="event_type"), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("metadata", sa.JSON()),
    )

    op.create_table(
        "alerts",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("type", sa.Enum("usage", "expiry", "academic", "system", name="alert_type"), nullable=False),
        sa.Column("title", sa.String(256), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("is_read", sa.Boolean(), default=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("alerts")
    op.drop_table("usage_events")
    op.drop_table("benefits")
    op.drop_table("course_results")
    op.drop_table("academic_records")
    op.drop_table("virtual_cards")
    op.drop_table("users")
    op.drop_table("tenants")
    op.execute("DROP TYPE IF EXISTS alert_type")
    op.execute("DROP TYPE IF EXISTS event_type")
    op.execute("DROP TYPE IF EXISTS benefit_category")
    op.execute("DROP TYPE IF EXISTS academic_status")
    op.execute("DROP TYPE IF EXISTS user_plan")
    op.execute("DROP TYPE IF EXISTS user_role")
    op.execute("DROP TYPE IF EXISTS tenant_plan")
