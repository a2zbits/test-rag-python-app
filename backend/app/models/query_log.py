from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, CreatedAtMixin, UUIDPrimaryKeyMixin


class QueryLog(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    """Minimal query log; retrieval/model details are deferred to later milestones."""

    __tablename__ = "query_logs"

    question: Mapped[str] = mapped_column(Text)
    latency_ms: Mapped[int | None]
