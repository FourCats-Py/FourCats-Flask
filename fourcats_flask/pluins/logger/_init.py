#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
from loguru import logger

from ._file_sink import FileSink
from ._filter import json_filter
from ._formatter import stderr_formatter, json_formatter


class InitLogger:

    def __init__(self, app_path: str, json_path: str = "", rotation: str = "00:00", retention: int = 6,
                 encoding: str = "UTF-8", spec: str = "YYYYMMDD", level: str = "INFO"):
        """
        loguru Document: https://loguru.readthedocs.io/en/stable/overview.html

        :param app_path: Absolute path of application log output file.
        :param json_path: Absolute path of log output file in JSON format.
        :param rotation: Document cutting method.
        :param retention: File backup method.
        :param encoding: Log file output code.
        :param spec: Log backup file output time style.
        :param level: Enter the log file log level.
        """
        app_file_sink = self.__init_file_sink(
            path=app_path, rotation=rotation, retention=retention, encoding=encoding, spec=spec
        )
        self.__init_app_log(app_file_sink, level=level)
        if json_path:
            json_file_sink = self.__init_file_sink(
                path=json_path, rotation=rotation, retention=retention, encoding=encoding, spec=spec
            )
            self.__init_json_log(json_file_sink, level=level)

    @staticmethod
    def __init_app_log(*args, **kwargs):
        """
        Initialize the application log.
        :param args:
        :param kwargs:
        :return:
        """
        logger.add(format=stderr_formatter, enqueue=True, *args, **kwargs)

    @staticmethod
    def __init_json_log(*args, **kwargs):
        """
        Initialize the JSON format log.
        :param args:
        :param kwargs:
        :return:
        """
        logger.add(format=json_formatter, enqueue=True, filter=json_filter, *args, **kwargs)

    @staticmethod
    def __init_file_sink(*args, **kwargs):
        """"""
        return FileSink(*args, **kwargs)
