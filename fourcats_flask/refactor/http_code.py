#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
from .response import ApiResponse


class GainSuccess(ApiResponse):
    code = 200
    message = "获取成功"
    state_code = 1


class UpdateSuccess(ApiResponse):
    code = 200
    message = "更新成功"
    state_code = 1


class CreateSuccess(ApiResponse):
    code = 201
    message = "创建成功"
    state_code = 1


class DeleteSuccess(ApiResponse):
    code = 204
    message = "删除成功"
    state_code = 1


class BadRequestException(ApiResponse):
    code = 400
    message = "客户端错误"
    state_code = 0


class AuthFailedException(ApiResponse):
    code = 401
    message = "认证失败"
    state_code = -1


class ForbiddenException(ApiResponse):
    code = 403
    message = "暂无权限"
    state_code = 0


class NotFoundException(ApiResponse):
    code = 404
    message = "没有找到资源"
    state_code = 0


class ParameterException(ApiResponse):
    code = 422
    message = "参数错误"
    state_code = 0


class ServerException(ApiResponse):
    code = 500
    message = "抱歉, 系统发生未知错误 (*￣︶￣)!"
    state_code = 0
