#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-23
import time

import jwt
from flask import g
from typing import Callable
from flask_httpauth import HTTPTokenAuth

from ..refactor.http_code import AuthFailedException


class Token:
    """"""

    def __init__(self, secret: str, scheme: str = "JWT", algorithm="HS256", message: str = "认证失败"):
        """"""
        self.secret = secret
        self.message = message
        self.algorithm = algorithm
        self.permission_callback = None
        self.auth = HTTPTokenAuth(scheme=scheme)
        self.init_app()

    def init_app(self):
        """"""
        @self.auth.verify_token
        def verify_token(token: str):
            """"""
            try:
                data = jwt.decode(token, self.secret, algorithms=self.algorithm)
            except jwt.exceptions.ExpiredSignatureError:
                raise AuthFailedException(message=self.message)
            except jwt.exceptions.InvalidSignatureError:
                raise AuthFailedException(message=self.message)
            except jwt.exceptions.DecodeError:
                raise AuthFailedException(message=self.message)

            user = data.get("user", dict())

            if self.permission_callback is not None:
                self.permission_callback(user)

            g.user = user
            return data
        return self

    def generate_token(self, user: dict = None, expiration: int = None) -> str:
        """生成令牌"""
        payload = dict()
        if user is not None:
            payload["user"] = user

        if expiration is not None:
            iat = int(time.time())
            payload["iat"] = iat
            payload["exp"] = iat + expiration

        token = jwt.encode(payload=payload, key=self.secret, algorithm=self.algorithm)
        return token

    def verify_permission(self, func: Callable):
        self.permission_callback = func
        return func
