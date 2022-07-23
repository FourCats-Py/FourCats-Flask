#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
import json
import certifi
import urllib3
from typing import Any, Callable

from loguru import logger

from .excepts import ExceptionError, ExceptionService


class Requester:
    """"""

    def __init__(self, method, url, fields=None, headers=None, q_type=None, **urlopen_kw):
        """"""
        if q_type is not None:
            func = getattr(self, q_type)
            self.__response = func(method=method, url=url, fields=fields, headers=headers, **urlopen_kw)
        else:
            self.__response = self.request_method(method=method, url=url, fields=fields, headers=headers, **urlopen_kw)

    @property
    def response(self):
        return self.__response

    def json_request(self, method, url, fields=None, headers=None, body=None, **urlopen_kw):
        """"""
        if headers is None:
            headers = dict()
        headers["Content-Type"] = "application/json; charset=utf-8"
        if not isinstance(body, str):
            body = json.dumps(body)
        return self.request_method(method=method, url=url, fields=fields, headers=headers, body=body, **urlopen_kw)

    def json_decode(self):
        """"""
        return json.loads(bytes.decode(self.__response.data))

    def check_result(self, check_filed: str, check_value: Any, exception: Callable = None, message_field: str = None,
                     message: Any = None):
        """"""
        result = json.loads(bytes.decode(self.__response.data))
        if result.get(check_filed, "") != check_value:
            if exception is None:
                return result

            if message_field is not None:
                _message = result.get(message_field, "")
                raise self.raise_exception(exception=exception, message=_message)
            raise self.raise_exception(exception=exception, message=message)
        return result

    @staticmethod
    def raise_exception(exception: Callable, message: Any = None):
        """"""
        if isinstance(message, str):
            raise exception(message)

        if isinstance(message, dict):
            raise exception(**message)

        if isinstance(message, (list, tuple)):
            raise exception(*message)

    @staticmethod
    def request_method(method, url, fields=None, headers=None, **urlopen_kw):
        """"""
        if (url is None or url == "") and (method is None or method == ""):
            raise ExceptionError("Request (URL / METHOD) cannot be empty or None.")

        try:
            logger.debug("".join(["*" * 30, " " * 5, "REQUEST START", " " * 5, "*" * 30]))
            logger.debug("METHOD: {}".format(method))
            logger.debug("URL: {}".format(url))
            logger.debug("HEADERS: {}".format(json.dumps({} if headers is None else headers)))
            logger.debug("FIELDS: {}".format(json.dumps({} if fields is None else fields)))
            logger.debug("BODY: {}".format(json.dumps(urlopen_kw.get("body", dict()), ensure_ascii=False)))
            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            response = http.request(method=method, url=url, headers=headers, fields=fields, **urlopen_kw)
            logger.debug("".join(["*" * 30, " " * 5, "REQUEST END", " " * 5, "*" * 30]))

            logger.debug("".join(["*" * 30, " " * 5, "RESPONSE START", " " * 5, "*" * 30]))
            try:
                result = bytes.decode(response.data)
            except Exception as e:
                logger.error(e)
                result = dict()
            logger.debug("RESPONSE: {}".format(result))
            logger.debug("".join(["*" * 30, " " * 5, "RESPONSE END", " " * 5, "*" * 30]))
        except Exception as e:
            logger.error(f"远端服务器调用失败 - {e}")
            raise ExceptionService("远端服务器调用失败~")
        return response
