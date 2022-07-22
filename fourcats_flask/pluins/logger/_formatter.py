#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
import datetime

from ._model import LoggerContent


class JsonFormatter:
    """
    自定义 Json 序列化
    """
    content = LoggerContent

    def __init__(self, record: dict):
        """"""
        # 清理无用内容
        extra = record.get("extra", dict()).copy()
        extra.pop("json_logger", "")

        # 拼接固定内容
        message = record.get("message", "")
        level = record.get("level", dict()).name
        fileline = ":".join([record["name"], record["function"], str(record["line"])])
        _datetime = record.get("time", datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S.%f")
        alias = extra.pop("alias", "")
        state = extra.pop("state", "")
        extra = extra
        self.__content = self.content(
            alias=alias, level=level, message=message, fileline=fileline, datetime=_datetime, state=state, extra=extra
        )

    @property
    def data(self) -> dict:
        """"""
        return self.__content.dict()

    @property
    def serialize(self) -> str:
        """"""
        return self.__content.json(ensure_ascii=False)


def json_formatter(record: dict) -> str:
    """"""
    record["extra"].pop("serialized", "")
    record["extra"]["serialized"] = JsonFormatter(record=record).serialize
    return "{extra[serialized]}\n"


def stderr_formatter(record: dict) -> str:
    """"""
    record["extra"].pop("serialized", "")
    json_logger = record["extra"].get("json_logger", False)
    if json_logger is True:
        record["extra"]["serialized"] = JsonFormatter(record=record).serialize
        formatter = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} - {message} - " \
                    "{extra[serialized]}\n"
    else:
        formatter = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} - {message}\n"
    return formatter
