#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
from mergedict import MergeDict


class Registry(object):
    """ Configuration module"""

    def __init__(self, options=None):
        if type(options) is dict:
            self.options = options
        else:
            self.options = {}
        self.hooks = {}

    def set(self, key, value):
        """Set configuration items."""
        items = key.split('.')
        if len(items) == 1:
            self.options[key] = value
            return self.get(key)
        end_key = items.pop()
        options = self.options
        for item in items:
            if options.get(item) is None:
                options.setdefault(item, {})
            if not isinstance(options.get(item), dict):
                options[item] = {}
            options = options.get(item)
        options[end_key] = value
        return self.get(key)

    def merge(self, key, value):
        """Merge configuration items."""
        if not isinstance(value, dict):
            return False
        news = MergeDict(self.get(key, {}))
        news.merge(value)
        self.set(key, news)
        return news

    def get(self, key=None, default=None, empty=False):
        """Get configuration items."""
        if key is None:
            return self.options
        items = key.split('.')
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
        """Set default values."""
        value = self.get(key)
        if value is None:
            self.get(key, default)
            return default
        return value

    def load(self, value):
        """Load configuration items."""
        if isinstance(value, dict):
            self.options.update(value)
            return True
        else:
            return False
