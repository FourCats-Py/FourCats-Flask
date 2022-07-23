#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
from flask import request
from flask_restx.reqparse import RequestParser as _RequestParser

from .http_code import ParameterException


class RequestParser(_RequestParser):
    """
    自定义参数解析器
    """

    def parse_args(self, req=None, strict=False):
        """
        Parse all arguments from the provided request and return the results as a ParseResult
        :rtype: ParseResult
        :param req:
        :param strict: if req includes args not in parser, throw 400 BadRequest exception
        :return: the parsed results as :class:`ParseResult` (or any class defined as :attr:`result_class`)
        """
        if req is None:
            req = request

        result = self.result_class()

        # A record of arguments not yet parsed; as each is found
        # among self.args, it will be popped out
        req.unparsed_arguments = dict(self.argument_class('').source(req)) if strict else {}
        errors = {}
        for arg in self.args:
            value, found = arg.parse(req, self.bundle_errors)
            if isinstance(value, ValueError):
                errors.update(found)
                found = None
            if found or arg.store_missing:
                result[arg.dest or arg.name] = value
        if errors:
            raise ParameterException(data=errors)

        if strict and req.unparsed_arguments:
            arguments = ', '.join(req.unparsed_arguments.keys())
            msg = 'Unknown arguments: {0}'.format(arguments)
            raise ParameterException(data=msg)

        return result
