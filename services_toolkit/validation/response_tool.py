from logging import getLogger

from typing import Dict, Tuple, Any
from flask import jsonify
from flask.wrappers import Response

LOGGER = getLogger(__name__)


def create_response(
        status: int = 200, message: str = None, headers: Dict[str, Any] = None, data: Dict[str, Any] = None
) -> Tuple[Response, int]:
    response = {
        status: status,
        message: message if message else '',
        headers: headers if headers else {},
        data: str(data) if data else {},
    }
    return jsonify(response), status
