from datetime import datetime, timezone
from logging import getLogger
from typing import Optional, Type

from flask import g, Response, request

from services_toolkit.integrations.sso_helper import SSOHelper

logger = getLogger(__name__)


def before_app_request(model: Type,
                       sso_client_id: Optional[str] = None) -> None:
    sso = SSOHelper(sso_client_id) if sso_client_id else None
    sso_payload = dict()
    if sso is not None:
        token, _ = sso.auth_header.extract()
        sso_payload = sso.extract_payload(token)
    sso_id = sso_payload.get('sub')
    data = request.data.decode()
    record = model.create(sso_id=sso_id,  # noqa
                          route=request.path,
                          method=request.method,
                          request=data)
    g.activities_record = record


def after_app_request(response: Response) -> Response:
    record = g.activities_record
    data = request.data.decode()
    if not record:
        return response
    record.update(duration=(datetime.now(timezone.utc) - record.ts).total_seconds(),
                  status=response.status,
                  response=data)
    return response
