#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-22
import typing as t
from flask.wrappers import Request as _Request


class Request(_Request):

    def get_json(
            self, force: bool = False, silent: bool = False, cache: bool = True
    ) -> t.Optional[t.Any]:
        """Parse :attr:`data` as JSON.

                If the mimetype does not indicate JSON
                (:mimetype:`application/json`, see :attr:`is_json`), or parsing
                fails, :meth:`on_json_loading_failed` is called and
                its return value is used as the return value. By default this
                raises a 400 Bad Request error.

                :param force: Ignore the mimetype and always try to parse JSON.
                :param silent: Silence mimetype and parsing errors, and
                    return ``None`` instead.
                :param cache: Store the parsed JSON to return for subsequent
                    calls.

                .. versionchanged:: 2.1
                    Raise a 400 error if the content type is incorrect.
                """
        if self.is_json is False:
            return dict()

        if cache and self._cached_json[silent] is not Ellipsis:
            return self._cached_json[silent]

        if not (force or self.is_json):
            if not silent:
                return self.on_json_loading_failed(None)
            else:
                return None

        data = self.get_data(cache=cache)

        try:
            rv = self.json_module.loads(data)
        except ValueError as e:
            if silent:
                rv = None

                if cache:
                    normal_rv, _ = self._cached_json
                    self._cached_json = (normal_rv, rv)
            else:
                rv = self.on_json_loading_failed(e)

                if cache:
                    _, silent_rv = self._cached_json
                    self._cached_json = (rv, silent_rv)
        else:
            if cache:
                self._cached_json = (rv, rv)

        return rv
