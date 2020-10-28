from logging import getLogger
from pathlib import Path

logger = getLogger(__name__)


def read_version(path: str) -> str:
    if not Path(path).exists():
        return '0.0.0'

    with open(path, encoding='utf-8') as file:
        version = file.readline().strip()
        logger.info('Current version: %s', version)

        return version
