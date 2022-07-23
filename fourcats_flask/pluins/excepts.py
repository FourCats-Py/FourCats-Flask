#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21


class ExceptionBase(Exception):
    """基础异常"""
    pass


class ExceptionService(ExceptionBase):
    """服务异常"""
    pass


class ExceptionServer(ExceptionBase):
    """服务异常"""
    pass


class ExceptionError(ExceptionBase):
    """错误异常"""
    pass


class ExceptionWarning(ExceptionBase):
    """警告异常"""
    pass


class ExceptionInfo(ExceptionBase):
    """消息异常"""
    pass
