import os
from logging import getLogger

logger = getLogger(__name__)


def read_version(path):
    if not os.path.isfile:
        return None

    with open(path, encoding='utf-8') as file:
        version = file.readline().strip()
        logger.info('Current version: %s', version)

        return version
