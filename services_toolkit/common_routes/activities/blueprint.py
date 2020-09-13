from functools import partial
from logging import getLogger
from typing import Optional

from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

from services_toolkit.common_routes.activities.callbacks import before_app_request, after_app_request
from services_toolkit.common_routes.activities.db import make_model

logger = getLogger(__name__)


def make_activities_blueprint(db: Optional[SQLAlchemy],  # pylint: disable=invalid-name
                              sso_client_id: Optional[str] = None) -> Blueprint:
    model = make_model(table_name='activities', db=db)
    blueprint = Blueprint('activities', __name__)
    blueprint.before_app_request(partial(before_app_request,
                                         model=model,
                                         sso_client_id=sso_client_id))
    blueprint.after_app_request(after_app_request)
    return blueprint
