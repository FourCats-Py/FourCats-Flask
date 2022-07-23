#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
import os
import glob
import locale

from loguru._ctime_functions import get_ctime, set_ctime
from loguru._datetime import datetime
from loguru._file_sink import FileSink as _FileSink, FileDateFormatter


def generate_rename_path(root, ext, creation_time, spec="%Y-%m-%d_%H-%M-%S_%f"):
    creation_datetime = datetime.fromtimestamp(creation_time)
    date = FileDateFormatter(creation_datetime)

    renamed_path = "{}{}.{}".format(root, ext, format(date, spec))
    counter = 1

    while os.path.exists(renamed_path):
        counter += 1
        renamed_path = "{}{}.{}.{}".format(root, ext, format(date, spec), counter)

    return renamed_path


class FileSink(_FileSink):

    def __init__(
            self,
            path,
            *,
            rotation=None,
            retention=None,
            compression=None,
            delay=False,
            mode="a",
            buffering=1,
            encoding=None,
            spec=None,
            **kwargs
    ):
        self.encoding = locale.getpreferredencoding(False) if encoding is None else encoding
        self.spec = spec
        self._kwargs = {**kwargs, "mode": mode, "buffering": buffering, "encoding": self.encoding}
        self._path = str(path)

        self._glob_patterns = self._make_glob_patterns(self._path)
        self._rotation_function = self._make_rotation_function(rotation)
        self._retention_function = self._make_retention_function(retention)
        self._compression_function = self._make_compression_function(compression)

        self._file = None
        self._file_path = None

        if not delay:
            self._initialize_file()

    def _terminate_file(self, *, is_rotating=False):
        old_path = self._file_path

        if self._file is not None:
            self._file.close()
            self._file = None
            self._file_path = None

        if is_rotating:
            new_path = self._prepare_new_path()

            if new_path == old_path:
                creation_time = get_ctime(old_path)
                root, ext = os.path.splitext(old_path)
                if self.spec is not None:
                    renamed_path = generate_rename_path(root, ext, creation_time, spec=self.spec)
                else:
                    renamed_path = generate_rename_path(root, ext, creation_time)
                os.rename(old_path, renamed_path)
                old_path = renamed_path

        if is_rotating or self._rotation_function is None:
            if self._compression_function is not None and old_path is not None:
                self._compression_function(old_path)

            if self._retention_function is not None:
                logs = {
                    file
                    for pattern in self._glob_patterns
                    for file in glob.glob(pattern)
                    if os.path.isfile(file)
                }
                self._retention_function(list(logs))

        if is_rotating:
            file = open(new_path, **self._kwargs)
            set_ctime(new_path, datetime.now().timestamp())

            self._file_path = new_path
            self._file = file
