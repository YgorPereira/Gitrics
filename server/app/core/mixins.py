from uuid import UUID, uuid4

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column


class IdMixin:
    """Mixin class for models with an id field."""

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
