from flask_sqlalchemy import SQLAlchemy

from services_toolkit.alchemy_mixins import TimeCastMixin


class CreatedAtMixin:
    def __new__(cls, db: SQLAlchemy):
        fields = dict(
            created_at=db.Column(db.DateTime(timezone=True),
                                 default=TimeCastMixin.utc_now),
            updated_at=db.Column(db.DateTime(timezone=True),
                                 default=TimeCastMixin.utc_now,
                                 onupdate=TimeCastMixin.utc_now)
        )
        return type('_CRUDMixin', (object,), fields)
