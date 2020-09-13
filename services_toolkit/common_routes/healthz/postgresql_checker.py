from logging import getLogger

from flask_sqlalchemy import SQLAlchemy

from services_toolkit.common_routes.healthz import CheckerBase

logger = getLogger(__name__)


class PostgresqlChecker(CheckerBase):

    def __init__(self, db: SQLAlchemy):
        super().__init__(name='postgresql', db=db)

    def checker(self, db: SQLAlchemy) -> bool:  # pylint: disable=arguments-differ
        is_passed: bool = False

        try:
            db.engine.execute('SELECT 1')
            is_passed = True
        except Exception:  # pylint: disable=broad-except
            logger.error('Health check failed:\n{err}')

        return is_passed
