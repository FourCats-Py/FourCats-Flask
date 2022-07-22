#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
import json
import contextvars


class LoggerContent:
    """"""
    __source = ""
    __source_type = ""
    __service_id = ""
    __uip = contextvars.ContextVar("Uip", default="")
    __trace_id = contextvars.ContextVar("TraceId", default="")

    def __init__(self, alias: str = "", level: str = "", message: str = "", fileline: str = "", datetime: str = "",
                 state: str = "", extra: dict = ""):
        """"""
        self.__alias = alias
        self.__level = level
        self.__message = message
        self.__fileline = fileline
        self.__datetime = datetime
        self.__state = state
        self.__extra = extra or dict()

    @property
    def source(self):
        """"""
        return self.__check_type(self.__source)

    @property
    def source_type(self):
        """"""
        return self.__check_type(self.__source_type)

    @property
    def service_id(self):
        """"""
        return self.__check_type(self.__service_id)

    @property
    def tag(self):
        """"""
        return self.__check_type(self.__alias).split(".")[0]

    @property
    def uip(self):
        """"""
        return self.__check_type(self.__uip.get())

    @property
    def trace_id(self):
        """"""
        return self.__check_type(self.__trace_id.get())

    @property
    def alias(self):
        """"""
        return self.__check_type(self.__alias)

    @property
    def level(self):
        """"""
        return self.__check_type(self.__level)

    @property
    def message(self):
        """"""
        return self.__check_type(self.__message)

    @property
    def fileline(self):
        """"""
        return self.__check_type(self.__fileline)

    @property
    def datetime(self):
        """"""
        return self.__check_type(self.__datetime)

    @property
    def state(self):
        """"""
        return self.__check_type(self.__state)

    @property
    def extra(self):
        """"""
        if not isinstance(self.__extra, dict):
            extra = dict()
        else:
            extra = self.__extra
        return json.dumps(extra, ensure_ascii=False)

    @classmethod
    def set_source(cls, value):
        """"""
        cls.__source = value

    @classmethod
    def set_source_type(cls, value):
        """"""
        cls.__source_type = value

    @classmethod
    def set_service_id(cls, value):
        """"""
        cls.__service_id = value

    @classmethod
    def set_uip(cls, value):
        """"""
        cls.__uip.set(value)

    @classmethod
    def set_trace_id(cls, value):
        """"""
        cls.__trace_id.set(value)

    @staticmethod
    def __check_type(value):
        if not isinstance(value, str):
            return ""
        return value

    def __getitem__(self, item):
        """"""
        return getattr(self, item)

    def dict(self, **kwargs):
        return dict(self, **kwargs)

    def json(self, *args, **kwargs):
        return json.dumps(self.dict(), *args, **kwargs)

    def keys(self):
        """"""
        return [
            "source", "source_type", "service_id", "tag", "uip", "trace_id", "alias", "level", "message", "fileline",
            "datetime", "state", "extra"
        ]
