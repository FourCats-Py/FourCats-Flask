#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
import json
import os.path
import time

from loguru import logger
from flask import g, request, Response

from ..refactor.api import Api


class GlobalLogger:
    """
    请求后打印自定义请求日志
    """

    def __init__(self, response: Response, api: Api, level: str = "info"):
        """"""
        try:
            self.__logger(response=response, api=api, level=level)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(e)

    def __logger(self, response: Response, api: Api, level: str = "info"):
        """
        打印日志
        :return:
        """

        method = request.method
        path = request.path
        swagger_dict = api.__schema__
        rule_basename = os.path.basename(request.url_rule.rule)
        if ":" in rule_basename:
            basename = "{" + rule_basename.split(":")[1].replace(">", "") + "}"
        else:
            basename = rule_basename.replace("<", "{").replace(">", "}")
        # 当做权限是，可以使用 request.url_rule.rule 作为路由信息，进行权限匹配
        rule = request.url_rule.rule.replace(rule_basename, basename)
        describe = swagger_dict.get("paths").get(rule, dict()).get(method.lower(), dict()).get("summary")
        params = self.__get_params(_request=request)
        uip = request.remote_addr
        http_code = response.status_code

        log_msg = {
            "describe": describe, "method": method, "path": path, "request": params, "uip": uip, "http_code": http_code,
            "response": json.loads(bytes.decode(response.data)) if response.data else list(),
            "request_time": g.request_time, "response_time": int(time.time()), "use_time": time.time() - g.request_time
        }
        if "swagger" not in path:
            getattr(logger, level)(json.dumps(log_msg, ensure_ascii=False))

    def __get_params(self, _request):
        """
        获取所有参数
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
        检测参数类型
        :param data: 参数
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
