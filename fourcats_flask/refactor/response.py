#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
import typing

if typing.TYPE_CHECKING:
    from _typeshed.wsgi import WSGIEnvironment

from flask import json, g
from werkzeug.exceptions import HTTPException


class ApiResponse(HTTPException):
    code = 500
    message = "Sorry, an unknown error occurred in the system. (*￣︶￣)!"
    state_code = 0

    def __init__(self, http_code=None, message=None, state_code=None, data=None, paging=False):
        if http_code is not None:
            self.code = http_code

        if message is not None:
            self.message = message

        if state_code is not None:
            self.state_code = state_code

        self.paging = paging
        self.data = data if data is not None else list()
        super(ApiResponse, self).__init__(message, None)

    def get_body(
            self,
            environ: typing.Optional["WSGIEnvironment"] = None,
            scope: typing.Optional[dict] = None,
    ) -> str:
        body = dict(message=self.message, code=self.state_code, timestamp=g.request_time, data=self.data)
        if self.paging:
            body["data"] = self.get_page(**self.data)
        return json.dumps(body)

    def get_headers(
            self,
            environ: typing.Optional["WSGIEnvironment"] = None,
            scope: typing.Optional[dict] = None,
    ) -> typing.List[typing.Tuple[str, str]]:
        return [("Content-Type", "application/json; charset=utf-8")]

    @staticmethod
    def get_page(total, page_total, page, pagesize, items):
        body = dict(total=total, page_total=page_total, page=page, pagesize=pagesize, items=items)
        return body
