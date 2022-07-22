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

        :param app_path: 应用日志输出文件绝对路径
        :param json_path: Json 格式日志输出文件绝对路径
        :param rotation: 文件切割方式, 详情请参考 `https://loguru.readthedocs.io/en/stable/overview.html?highlight=rotation#easier-file-logging-with-rotation-retention-compression`
        :param retention: 文件备份方式, 详情请参考 `https://loguru.readthedocs.io/en/stable/overview.html?highlight=rotation#easier-file-logging-with-rotation-retention-compression`
        :param encoding: 日志文件输出编码
        :param spec: 日志备份文件输出时间样式
        :param level: 输入日志文件日志级别
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
        """"""
        logger.add(format=stderr_formatter, enqueue=True, *args, **kwargs)

    @staticmethod
    def __init_json_log(*args, **kwargs):
        """"""
        logger.add(format=json_formatter, enqueue=True, filter=json_filter, *args, **kwargs)

    @staticmethod
    def __init_file_sink(*args, **kwargs):
        """"""
        return FileSink(*args, **kwargs)
