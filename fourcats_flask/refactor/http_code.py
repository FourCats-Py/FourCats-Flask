#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
from .response import ApiResponse


class GainSuccess(ApiResponse):
    code = 200
    message = "Success"
    state_code = 1


class UpdateSuccess(ApiResponse):
    code = 200
    message = "Update success"
    state_code = 1


class CreateSuccess(ApiResponse):
    code = 201
    message = "Created success"
    state_code = 1


class DeleteSuccess(ApiResponse):
    code = 204
    message = "Deleted success"
    state_code = 1


class BadRequestException(ApiResponse):
    code = 400
    message = "Client error"
    state_code = 0


class AuthFailedException(ApiResponse):
    code = 401
    message = "Authentication failed"
    state_code = -1


class ForbiddenException(ApiResponse):
    code = 403
    message = "Forbidden"
    state_code = 0


class NotFoundException(ApiResponse):
    code = 404
    message = "NotFound"
    state_code = 0


class ParameterException(ApiResponse):
    code = 422
    message = "Parameter error"
    state_code = 0


class ServerException(ApiResponse):
    code = 500
    message = "Sorry, an unknown error occurred in the system. (*￣︶￣)!"
    state_code = 0
