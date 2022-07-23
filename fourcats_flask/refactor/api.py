#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
from __future__ import unicode_literals

import six
import sys

from flask_restx import Api as _Api
from flask_restx.utils import unpack
from flask import request, current_app
from flask_restx._http import HTTPStatus
from werkzeug.datastructures import Headers
from flask_restx.api import HEADERS_BLACKLIST
from flask.signals import got_request_exception
from flask import make_response as original_flask_make_response
from werkzeug.exceptions import HTTPException, NotAcceptable, InternalServerError

from .response import ApiResponse


class Api(_Api):

    def make_response(self, data, *args, **kwargs):
        """
        Looks up the representation transformer for the requested media
        type, invoking the transformer to create a response object. This
        defaults to default_mediatype if no transformer is found for the
        requested mediatype. If default_mediatype is None, a 406 Not
        Acceptable response will be sent as per RFC 2616 section 14.1

        :param data: Python object containing response data to be transformed
        :param data:
        :param args:
        :param kwargs:
        :return:
        """

        default_mediatype = kwargs.pop('fallback_mediatype', None) or self.default_mediatype
        mediatype = request.accept_mimetypes.best_match(
            self.representations,
            default=default_mediatype,
        )
        if mediatype is None:
            raise NotAcceptable()

        if isinstance(data, ApiResponse):
            return data

        if mediatype in self.representations:
            resp = self.representations[mediatype](data, *args, **kwargs)
            resp.headers['Content-Type'] = mediatype
            return resp
        elif mediatype == 'text/plain':
            resp = original_flask_make_response(str(data), *args, **kwargs)
            resp.headers['Content-Type'] = 'text/plain'
            return resp
        else:
            raise InternalServerError()

    def handle_error(self, e):
        """
        Error handler for the API transforms a raised exception into a Flask response,
        with the appropriate HTTP status code and body.

        :param Exception e: the raised Exception object
        :param e:
        :return:
        """
        got_request_exception.send(current_app._get_current_object(), exception=e)

        if not isinstance(e, HTTPException) and current_app.propagate_exceptions:
            exc_type, exc_value, tb = sys.exc_info()
            if exc_value is e:
                raise
            else:
                raise e

        include_message_in_response = current_app.config.get("ERROR_INCLUDE_MESSAGE", True)
        default_data = {}

        headers = Headers()

        for typecheck, handler in six.iteritems(self._own_and_child_error_handlers):
            if isinstance(e, typecheck):
                result = handler(e)
                default_data, code, headers = unpack(result, HTTPStatus.INTERNAL_SERVER_ERROR)
                break
        else:
            if isinstance(e, HTTPException):
                code = HTTPStatus(e.code)
                if include_message_in_response:
                    default_data = {
                        'message': getattr(e, 'description', code.phrase)
                    }
                headers = e.get_response().headers
            elif self._default_error_handler:
                result = self._default_error_handler(e)
                default_data, code, headers = unpack(result, HTTPStatus.INTERNAL_SERVER_ERROR)
            else:
                code = HTTPStatus.INTERNAL_SERVER_ERROR
                if include_message_in_response:
                    default_data = {
                        'message': code.phrase,
                    }

        if include_message_in_response:
            default_data['message'] = default_data.get('message', str(e))

        data = getattr(e, 'data', default_data)
        fallback_mediatype = None

        if code >= HTTPStatus.INTERNAL_SERVER_ERROR:
            exc_info = sys.exc_info()
            if exc_info[1] is None:
                exc_info = None
            current_app.log_exception(exc_info)

        elif code == HTTPStatus.NOT_FOUND and current_app.config.get("ERROR_404_HELP", True) \
                and include_message_in_response:
            data['message'] = self._help_on_404(data.get('message', None))

        elif code == HTTPStatus.NOT_ACCEPTABLE and self.default_mediatype is None:
            # if we are handling NotAcceptable (406), make sure that
            # make_response uses a representation we support as the
            # default mediatype (so that make_response doesn't throw
            # another NotAcceptable error).
            supported_mediatypes = list(self.representations.keys())
            fallback_mediatype = supported_mediatypes[0] if supported_mediatypes else "text/plain"

        # Remove blacklisted headers
        for header in HEADERS_BLACKLIST:
            headers.pop(header, None)
        if isinstance(e, ApiResponse):
            e.data = data
            resp = self.make_response(e, code, headers, fallback_mediatype=fallback_mediatype)
        else:
            resp = self.make_response(data, code, headers, fallback_mediatype=fallback_mediatype)

        if code == HTTPStatus.UNAUTHORIZED:
            resp = self.unauthorized(resp)
        return resp
