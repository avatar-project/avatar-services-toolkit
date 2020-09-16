from datetime import datetime, timezone
from logging import getLogger
from typing import Optional, Type

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Text, Float, DateTime, Integer

from services_toolkit.alchemy_mixins import CRUDMixin

logger = getLogger(__name__)


def make_model(table_name: str, db: Optional[SQLAlchemy]) -> Type:  # pylint: disable=invalid-name,
    model = type(
        'ActivitiesModel', (
            CRUDMixin(db),
            db.Model
        ), dict(
            __tablename__=table_name,
            id=Column(Integer(), primary_key=True),
            sso_id=Column(String(), nullable=True, default=None),
            route=Column(String(), nullable=False),
            method=Column(String(10), nullable=False),
            request=Column(Text(), nullable=False),
            response=Column(Text(), nullable=True),
            ts=Column(DateTime(timezone=True), nullable=False,
                         default=datetime.utcnow().replace(tzinfo=timezone.utc)),
            duration=Column(Float(), nullable=True),
            status=Column(String, nullable=True),
        ))
    return model
