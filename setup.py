#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-23
import re
from setuptools import find_packages, setup

with open("fourcats_flask/__init__.py", "r") as file:
    regex_version = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    version = re.search(regex_version, file.read(), re.MULTILINE).group(1)

with open("README.md", "rb") as file:
    readme = file.read().decode("utf-8")


setup(
    name="fourcats-flask",
    version=version,
    packages=find_packages(),
    description="A flask encapsulated based on personal habits for fast use.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="ShiWeiDong",
    author_email="shiweidong1993@gmail.com",
    url="https://github.com/FourCats-Py/FourCats-Flask",
    download_url="https://github.com/FourCats-Py/FourCats-Flask/archive/{}.tar.gz".format(version),
    keywords=["fourcats", "flask"],
    install_requires=[
        "flask-restx>=0.5.1", "loguru>=0.6.0", "PyYAML>=6.0", "Flask-HTTPAuth>=4.7.0", "mergedict>=1.0.0",
        "urllib3>=1.26.10",  "Flask-SQLAlchemy>=2.5.1", "Flask-Cors>=3.0.10", "PyJWT>=2.4.0"
    ],
    python_requires=">=3.8"
)
