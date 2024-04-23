#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
import uuid
import time
import decimal
import traceback
import dataclasses
from typing import Union, Type
from datetime import date, datetime

from flask import g
from flask import Flask as _Flask
from flask.json.provider import JSONProvider
from werkzeug.exceptions import HTTPException
from flask.json.provider import DefaultJSONProvider as _DefaultJSONProvider

from .api import Api
from .sqlalchemy import db
from .requester import Request
from .response import ApiResponse
from ..pluins.global_logger import GlobalLogger
from .http_code import ServerException


class DefaultJSONProvider(_DefaultJSONProvider):

    @staticmethod
    def default(o):
        if hasattr(o, "keys") and hasattr(o, "__getitem__"):
            return dict(o)

        if isinstance(o, date):
            return o.strftime("%Y-%m-%d")

        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")

        if isinstance(o, (decimal.Decimal, uuid.UUID)):
            return str(o)

        if dataclasses and dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)

        if hasattr(o, "__html__"):
            return str(o.__html__())

        raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")


class Flask(_Flask):
    request_class: Type[Request] = Request
    json_provider_class: Type[JSONProvider] = DefaultJSONProvider


class FlaskInit:
    """"""

    @classmethod
    def register_api(cls, app: Flask, api: Api, hook: bool = False):
        """"""
        api.init_app(app=app)

        if hook is True:
            cls.register_hook(app=app, api=api)
        return

    @classmethod
    def register_config(cls, app: Flask, configs: Union[str, list], sqlalchemy: bool = False,
                        create_all: bool = False) -> None:
        """"""
        if not isinstance(configs, list):
            configs = [configs]

        for config in configs:
            app.config.from_object(config)

        if sqlalchemy is True:
            cls.register_sqlalchemy(app=app, create_all=create_all)

        return

    @classmethod
    def register_sqlalchemy(cls, app: Flask, create_all: bool = False) -> None:
        """"""
        db.init_app(app)

        if create_all is True:
            with app.app_context():
                db.create_all()
        return

    @classmethod
    def register_hook(cls, app: Flask, api: Api) -> None:
        """"""

        @app.errorhandler(Exception)
        def error_handler(e):
            """"""
            if isinstance(e, ApiResponse):
                return e
            if isinstance(e, HTTPException):
                if e.code == 500:
                    state_code = -1
                else:
                    state_code = 0
                return ApiResponse(http_code=e.code, message=e.description, state_code=state_code)
            else:
                if app.config['DEBUG'] is True:
                    traceback.print_exc()
                    return ServerException()
                else:
                    return ServerException()

        @app.after_request
        def after_request(response):
            """"""
            content_type = response.headers.get("Content-Type")
            if "application/json" in content_type:
                GlobalLogger(response=response, api=api)
            return response

        @app.before_request
        def before_request():
            """"""
            g.request_time = int(time.time())

        return
