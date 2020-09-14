from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy


class CreatedAtMixin:
    def __new__(cls, db: SQLAlchemy):
        fields = dict(
            created_at=db.Column(db.DateTime(timezone=True),
                                 default=datetime.utcnow().replace(tzinfo=timezone.utc)),
            updated_at=db.Column(db.DateTime(timezone=True),
                                 default=datetime.utcnow().replace(tzinfo=timezone.utc),
                                 onupdate=datetime.utcnow().replace(tzinfo=timezone.utc))
        )
        return type('_CreatedAtMixin', (object,), fields)
