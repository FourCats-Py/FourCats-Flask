#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
import json
import os.path
import time

from fourcats_utils import logger
from flask import g, request, Response

from ..refactor.api import Api


class GlobalLogger:
    """
    Print custom request log after request.
    """

    def __init__(self, response: Response, api: Api, level: str = "info"):
        """"""
        try:
            if "swagger" not in request.path:
                self.__logger(response=response, api=api, level=level)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(e)

    def __logger(self, response: Response, api: Api, level: str = "info"):
        """
        Print logs.
        :return:
        """

        method = request.method
        path = request.path
        swagger_dict = api.__schema__

        if request.url_rule is not None:
            rule_basename = os.path.basename(request.url_rule.rule)
            if ":" in rule_basename:
                basename = "{" + rule_basename.split(":")[1].replace(">", "") + "}"
            else:
                basename = rule_basename.replace("<", "{").replace(">", "}")
            rule = request.url_rule.rule.replace(rule_basename, basename)
        else:
            rule = ""

        describe = swagger_dict.get("paths").get(rule, dict()).get(method.lower(), dict()).get("summary")
        params = self.__get_params(_request=request)
        uip = request.remote_addr
        http_code = response.status_code

        log_msg = {
            "describe": describe, "method": method, "path": path, "request": params, "uip": uip, "http_code": http_code,
            "response": json.loads(bytes.decode(response.data)) if response.data else list(),
            "request_time": g.request_time, "response_time": int(time.time()), "use_time": time.time() - g.request_time
        }

        getattr(logger, level)(json.dumps(log_msg, ensure_ascii=False))

    def __get_params(self, _request):
        """
        Get all parameters.
        :return:
        """
        parameter = dict()
        parameter["data"] = self.__change(_request.data)
        parameter["args"] = self.__change(_request.args)
        parameter["form"] = self.__change(_request.form)
        if _request.is_json is True:
            parameter["json"] = self.__change(_request.json)
        else:
            parameter["json"] = dict()
        parameter["values"] = self.__change(_request.values)
        return parameter

    @staticmethod
    def __change(data):
        """
        Detect the parameter type.
        :param data: parameter
        :return:
        """
        result = data
        if isinstance(data, bytes):
            result = bytes.decode(data)
            if result:
                try:
                    result = json.loads(result)
                except json.decoder.JSONDecodeError as e:
                    logger.error(f"{e} - {result}")
            else:
                result = None
        return dict() if result is None else result
