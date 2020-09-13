from datetime import datetime, timezone
from logging import getLogger
from typing import Optional, Type

from flask_sqlalchemy import SQLAlchemy

from services_toolkit.alchemy_mixins import CRUDMixin

logger = getLogger(__name__)


def make_model(table_name: str, db: Optional[SQLAlchemy]) -> Type:  # pylint: disable=invalid-name,
    model = type(
        'ActivitiesModel', (
            CRUDMixin(db),
            db.Model
        ), dict(
            __tablename__=table_name,
            id=db.Column(db.Integer(), primary_key=True),
            sso_id=db.Column(db.String(), nullable=True, default=None),
            route=db.Column(db.String(), nullable=False),
            method=db.Column(db.String(10), nullable=False),
            request=db.Column(db.Text(), nullable=False),
            response=db.Column(db.Text(), nullable=True),
            ts=db.Column(db.DateTime(timezone=True), nullable=False,
                         default=datetime.utcnow().replace(tzinfo=timezone.utc)),
            duration=db.Column(db.Float(), nullable=True),
            status=db.Column(db.String, nullable=True),
        ))
    return model
