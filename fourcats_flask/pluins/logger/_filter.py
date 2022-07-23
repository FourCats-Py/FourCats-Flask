#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21

def json_filter(record: dict) -> bool:
    json_logger = record["extra"].get("json_logger", False)
    return json_logger
