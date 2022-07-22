#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
from mergedict import MergeDict


class Registry(object):
    """ 配置模块"""

    def __init__(self, options=None):
        if type(options) is dict:
            self.options = options
        else:
            self.options = {}
        self.hooks = {}

    def set(self, key, value):
        """设置配置项"""
        items = key.split('.')
        # 只需要设置顶层
        if len(items) == 1:
            self.options[key] = value
            return self.get(key)
        # 弹出最后的键
        end_key = items.pop()
        # 执行默认值处理
        options = self.options
        for item in items:
            if options.get(item) is None:
                options.setdefault(item, {})
            if not isinstance(options.get(item), dict):
                options[item] = {}
            options = options.get(item)
        # 设置新值
        options[end_key] = value
        return self.get(key)

    def merge(self, key, value):
        """合并配置项"""
        if not isinstance(value, dict):
            return False
        news = MergeDict(self.get(key, {}))
        news.merge(value)
        self.set(key, news)
        return news

    def get(self, key=None, default=None, empty=False):
        """获取配置项"""
        if key is None:
            return self.options
        items = key.split('.')
        # 处理数据
        options = self.options
        for item in items:
            options = options.get(item)
            if options is None:
                return default
        if empty:
            if not options:
                return default
        return options

    def default(self, key=None, default=None):
        """设置默认值"""
        value = self.get(key)
        if value is None:
            self.get(key, default)
            return default
        return value

    def load(self, value):
        """加载配置项"""
        if isinstance(value, dict):
            self.options.update(value)
            return True
        else:
            return False
