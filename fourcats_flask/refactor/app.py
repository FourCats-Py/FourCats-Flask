#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
import time
import traceback
from typing import Union
from decimal import Decimal
from datetime import date, datetime

from flask import g, current_app
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from .api import Api
from .sqlalchemy import db
from .requester import Request
from .response import ApiResponse
from ..pluins.global_logger import GlobalLogger
from .http_code import ServerException, NotFoundException


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        self.ensure_ascii = False
        if hasattr(o, "keys") and hasattr(o, "__getitem__"):
            return dict(o)
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, date):
            return o.strftime("%Y-%m-%d")
        if isinstance(o, Decimal):
            return o.__float__()
        raise ServerException()


class Flask(_Flask):
    request_class = Request
    json_encoder = JSONEncoder


class FlaskInit:
    """"""

    def __init__(self, api: Api, configs: Union[str, list], create_all: bool = False):
        """"""
        self.api = api
        self.configs = configs
        self.create_all = create_all

    def init_app(self, app: Flask):
        """"""
        self.register_config(app=app, configs=self.configs)
        self.register_sqlalchemy(app=app, create_all=self.create_all)
        self.register_hook(app=app, api=self.api)

    @staticmethod
    def register_config(app: Flask, configs: Union[str, list]) -> None:
        """"""
        if not isinstance(configs, list):
            configs = [configs]

        for config in configs:
            app.config.from_object(config)
        return

    @staticmethod
    def register_sqlalchemy(app: Flask, create_all: bool = False) -> None:
        """"""
        db.init_app(app)

        if create_all is True:
            with app.app_context():
                db.create_all()
        return

    @staticmethod
    def register_hook(app: Flask, api: Api) -> None:
        """"""

        @app.errorhandler(Exception)
        def error_handler(e):
            """"""
            if isinstance(e, ApiResponse):
                return e
            elif isinstance(e, ApiResponse):
                if e.code == 404:
                    return NotFoundException()
                return ServerException()
            else:
                if current_app.config["DEBUG"]:
                    traceback.print_exc()
                    return ServerException()
                else:
                    data = traceback.format_exc()
                    return ServerException(data=data)

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
