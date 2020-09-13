from datetime import timedelta, datetime, timezone
from logging import getLogger
from typing import Optional

from environs import Env
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

from services_toolkit.integrations.sso_helper import SSOHelper

USER_ONLINE_STATE_TTL = timedelta(seconds=10)

env = Env()
logger = getLogger(__name__)


class SSOUserMixin:
    def __new__(cls, db: SQLAlchemy):
        fields = dict(
            sso_id=db.Column(db.String, nullable=False, index=True),
            latest_session_started_at=db.Column(db.DateTime(timezone=timezone.utc), nullable=True, default=None),
            latest_session_request_at=db.Column(db.DateTime(timezone=timezone.utc), nullable=True, default=None),
        )
        return type('_SSOUserMixin', (SSOUserBase,), fields)


class SSOUserBase:

    sso_id = None
    latest_session_started_at = None
    latest_session_request_at = None

    @classmethod
    def auth_callback(cls: type,
                      token: str):

        config_client_id = current_app.config.get('SSO_CLIENT_ID')
        sso_client_id = config_client_id or env.str('SSO_CLIENT_ID', default='digital-avatar')

        is_verify = current_app.config.get('SSO_VERIFY_TOKEN') or True

        sso_helper = SSOHelper(client_id=sso_client_id)
        payload = sso_helper.extract_payload(token=token, verify=is_verify)

        sso_id = payload['sub']
        user = cls.ensure(sso_id=sso_id)  # pylint: disable=no-member
        user.update(latest_session_request_at=datetime.utcnow().replace(tzinfo=timezone.utc))

        return user

    @property
    def is_online(self) -> Optional[bool]:
        online_state: Optional[bool] = None
        if self.latest_session_request_at:
            time_delta: timedelta = datetime.utcnow() - self.latest_session_request_at
            online_state = USER_ONLINE_STATE_TTL >= time_delta
        return online_state

    @property
    def latest_session_duration(self) -> Optional[timedelta]:
        if not self.latest_session_request_at and not self.latest_session_started_at:
            return None
        session_duration = self.latest_session_request_at - self.latest_session_started_at
        if not self.is_online:
            session_duration += USER_ONLINE_STATE_TTL
        return session_duration

    def update_latest_session_time(self) -> datetime:
        timestamp = datetime.utcnow().replace(tzinfo=timezone.utc)
        if not self.is_online:
            logger.info(f'User {self.sso_id} came back')
            self.update(latest_session_started_at=timestamp)  # pylint: disable=no-member
        self.update(latest_session_request_at=timestamp)  # pylint: disable=no-member
        return timestamp