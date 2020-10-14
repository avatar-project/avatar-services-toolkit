import traceback
from enum import IntEnum, unique
from functools import wraps
from logging import getLogger
from typing import Type, Optional, Union, Tuple, Sequence, Set, Callable

from flask import request, jsonify
from marshmallow import Schema, ValidationError
from werkzeug import Response, exceptions  # noqa: PyPackageRequirements

logger = getLogger(__name__)

DEFAULT_VALIDATE_METHOD = 'GET'


@unique
class HTTPCodes(IntEnum):
    OK = 200
    BAD_REQUEST = 400
    UNPROCESSABLE_ENTITY = 422
    SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501


class route_validator:  # pylint: disable=invalid-name

    def __init__(self,
                 request_schema: Optional[Type[Schema]] = None,
                 response_schema: Optional[Type[Schema]] = None,
                 methods: Union[str, Sequence[str]] = DEFAULT_VALIDATE_METHOD):

        self.request_schema = request_schema() if request_schema else None
        self.response_schema = response_schema() if response_schema else None
        self.methods: Set[str] = set(m.upper().strip() for m in methods)
        self.log_prefix = None

    @staticmethod
    def _make_response(result: dict, status: int):
        return jsonify(headers=dict(),
                       message='',
                       success=status == HTTPCodes.OK,
                       result=result), status

    def _validate_request(self, _request):

        if not self.request_schema:
            return None

        if not _request.is_json:
            logger.warning(f'{self.log_prefix} < invalid content-type header')
            return self._make_response(status=HTTPCodes.BAD_REQUEST,
                                       result=dict(error='content-type'))

        try:
            self.request_schema.load(_request.json)
            logger.debug(f'{self.log_prefix} request body validated')
            return None
        except exceptions.BadRequest:
            logger.warning(f'{self.log_prefix} < invalid request body')
            return self._make_response(status=HTTPCodes.BAD_REQUEST,
                                       result=dict(error='invalid requests body'))
        except ValidationError as err:
            return self._make_response(status=HTTPCodes.UNPROCESSABLE_ENTITY,
                                       result=dict(error=err.messages))

    def _validate_def_call(self, func: Callable, *args, **kw):
        try:
            result = func(*args, **kw)
            response, status = result if isinstance(result, tuple) else (result, HTTPCodes.OK)
            if not isinstance(response, Response):
                response = jsonify(result)
            return response, status
        except NotImplementedError:
            response, status = self._make_response(status=HTTPCodes.NOT_IMPLEMENTED,
                                                   result=dict(error='NOT_IMPLEMENTED'))
            return response, status
        except Exception as err:  # pylint: disable=broad-except
            logger.error(f'{self.log_prefix} < {err}')
            response, status = self._make_response(status=HTTPCodes.SERVER_ERROR,
                                                   result=dict(error=str(traceback.format_exc())))
            return response, status

    def _validate_response(self, response, status):
        if not self.response_schema:
            return response, status

        if response.status_code != HTTPCodes.OK:
            return response, status

        try:
            data = self.response_schema.load(response.json)
            logger.debug(f'{self.log_prefix} response validated')
            response = jsonify(self.response_schema.dump(data))
        except (exceptions.BadRequest, ValidationError, TypeError) as err:
            logger.error(f'{self.log_prefix} < {err}')
            response, status = self._make_response(status=HTTPCodes.SERVER_ERROR,
                                                   result=dict(error=str(traceback.format_exc())))
        finally:
            return response, status  # pylint: disable=lost-exception

    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kw) -> Union[str, Tuple[Response, int]]:

            self.log_prefix = f'[ VALIDATION | {request.remote_addr} {request.method} > {request.url_rule} ]'

            if request.method not in self.methods:
                logger.debug(f'{self.log_prefix} skip {request.method} method, validator expect {self.methods}')
                return func(*args, **kw)

            error = self._validate_request(request)
            if error:
                response, status = error
                return response, status

            response, status = self._validate_def_call(func, *args, **kw)
            response, status = self._validate_response(response, status)

            return response, status

        return wrapper
