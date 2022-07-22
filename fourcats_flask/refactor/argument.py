#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
from flask_restx.reqparse import Argument as _Argument, _handle_arg_type, LOCATIONS


class Argument(_Argument):

    @property
    def __schema__(self):
        if self.location == 'cookie':
            return
        param = {
            'name': self.name,
            'in': LOCATIONS.get(self.location[-1], 'args') if isinstance(self.location,
                                                                         (tuple, list)) else LOCATIONS.get(
                self.location, 'args')
        }
        _handle_arg_type(self, param)
        if self.required:
            param['required'] = True
        if self.help:
            param['description'] = self.help
        if self.default is not None:
            param['default'] = self.default() if callable(self.default) else self.default
        if self.action == 'append':
            param['items'] = {'type': param['type']}
            param['type'] = 'array'
            param['collectionFormat'] = 'multi'
        if self.action == 'split':
            param['items'] = {'type': param['type']}
            param['type'] = 'array'
            param['collectionFormat'] = 'csv'
        if self.choices:
            param['enum'] = self.choices
            param['collectionFormat'] = 'multi'
        return param
