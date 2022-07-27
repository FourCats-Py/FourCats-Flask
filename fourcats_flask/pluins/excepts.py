#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21


class ExceptionBase(Exception):
    """Basic abnormality"""
    pass


class ExceptionService(ExceptionBase):
    """Service exception"""
    pass


class ExceptionServer(ExceptionBase):
    """Service exception"""
    pass


class ExceptionError(ExceptionBase):
    """Error exception"""
    pass


class ExceptionWarning(ExceptionBase):
    """Warning exception"""
    pass


class ExceptionInfo(ExceptionBase):
    """Message exception"""
    pass
