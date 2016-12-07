#!  /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_PATH)

# 课程配置
COURSES = {
    "Python": {
        "cycle": {
            "min": 24,
            "max": 52
        },
        "price": {
            "min": 6500,
            "max": 24000
        },
        "salary": {
            "min": 18000,
            "max": 50000
        },
        "location": ["beijing"]
    },
    "Linux": {
        "cycle": {
            "min": 12,
            "max": 36
        },
        "price": {
            "min": 4000,
            "max": 18000
        },
        "salary": {
            "min": 15000,
            "max": 60000
        },
        "location": ["beijing"]
    },
    "Golang": {
        "cycle": {
            "min": 24,
            "max": 52
        },
        "price": {
            "min": 5500,
            "max": 26000
        },
        "salary": {
            "min": 20000,
            "max": 65000
        },
        "location": ["shanghai"]
    }
}
