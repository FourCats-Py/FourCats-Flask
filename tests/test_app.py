#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2024/4/23
import time
import random
import string
import unittest

from example.create_flask import flask_app as app


class TestFlaskApi(unittest.TestCase):
    """"""

    def setUp(self):
        """"""
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        """"""
        time.sleep(5)

    @staticmethod
    def generate_random_string(min_length=5, max_length=10):
        """"""
        length = random.randint(min_length, max_length)
        letters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

    def generate_params(self):
        """"""
        return (
            random.randint(10000, 100000),
            self.generate_random_string(),
            self.generate_random_string(),
            self.generate_random_string()
        )

    def test_get(self):
        """"""
        pid, a, b, c = self.generate_params()
        compare = dict(pid=pid, a=a, b=b, c=c)
        response = self.app.get(f"/api/test/{pid}?a={a}&b={b}&c={c}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("data"), compare)

    def test_post(self):
        """"""
        pid, a, b, c = self.generate_params()
        compare = dict(pid=pid, a=a, b=b, c=c)
        response = self.app.post(f"/api/test/{pid}?c={c}", json={"a": a, "b": b})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get("data"), compare)

    def test_patch(self):
        """"""
        pid, a, b, c = self.generate_params()
        compare = dict(pid=pid, a=a, b=b, c=c)
        response = self.app.patch(f"/api/test/{pid}?c={c}", json={"a": a, "b": b})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("data"), compare)

    def test_put(self):
        """"""
        pid, a, b, c = self.generate_params()
        compare = dict(pid=pid, a=a, b=b, c=c)
        response = self.app.put(f"/api/test/{pid}?c={c}", json={"a": a, "b": b})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("data"), compare)

    def test_delete(self):
        """"""
        pid, a, b, c = self.generate_params()
        response = self.app.delete(f"/api/test/{pid}?a={a}&b={b}&c={c}")
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
