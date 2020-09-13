from services_toolkit.common_routes.activities.blueprint import make_activities_blueprint
from services_toolkit.common_routes.healthz.routes import make_healthz_blueprint
from services_toolkit.common_routes.swagger import make_swagger

__all__ = (
    'make_healthz_blueprint',
    'make_activities_blueprint',
    'make_swagger',
)
