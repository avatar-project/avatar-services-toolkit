from typing import Dict, Tuple, Any

from flask import jsonify
from flask.wrappers import Response


def create_response(
        status: int = 200, message: str = None, headers: Dict[str, Any] = None, data: Dict[str, Any] = None
) -> Tuple[Response, int]:
    response = {
        'status': status,
        'message': message or '',
        'headers': headers or {},
        'data': data or {},
    }
    return jsonify(response), status
