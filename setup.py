#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-23
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("fourcats_flask/__init__.py", "r") as file:
    regex_version = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    version = re.search(regex_version, file.read(), re.MULTILINE).group(1)

with open("README.md", "rb") as file:
    readme = file.read().decode("utf-8")


setup(
    name="fourcats-flask",
    version=version,
    packages=["fourcats_flask"],
    description="A quick use tool for Python common connectors.",
    long_description=readme,
    long_description_content_type="text/x-rst",
    author="ShiWeiDong",
    author_email="weidong_shi@outlook.com",
    url="https://github.com/FourCats-Py/FourCats-Flask",
    download_url="https://github.com/FourCats-Py/FourCats-Flask/archive/{}.tar.gz".format(version),
    keywords=["fourcats", "flask"],
    install_requires=[
        "flask-restx>=0.5.1", "loguru>=0.6.0", "PyYAML>=6.0",
        "urllib3>=1.26.10",  "Flask-SQLAlchemy>=2.5.1", "Flask-Cors>=3.0.10"
    ],
    python_requires=">=3.8"
)