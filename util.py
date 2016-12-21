#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import _pickle
import functools


def pickle_to_file(filepath, obj):
    """dump对象到文件"""
    with open(filepath, mode='wb') as f:
        pick = _pickle.Pickler(f)
        pick.dump(obj)


def upickle_from_file(filepath):
    """从文件中load对象并返回"""

    obj = {}
    if os.path.isfile(filepath):
        with open(filepath, mode='rb') as f:
            upick = _pickle.Unpickler(f)
            obj = upick.load()
    return obj


def auth(before_fn=None, after_fn=None):

    def decorator(fn_or_cls):
        @functools.wraps(fn_or_cls)
        def wrapper(*args, **kwargs):
            if before_fn:
                before_fn()
            obj = fn_or_cls(*args, **kwargs)
            if after_fn:
                after_fn()
            return obj
        return wrapper
    return decorator
