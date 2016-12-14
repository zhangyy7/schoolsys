#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import _pickle


def pickle_to_file(filepath, obj):
    """dump对象到文件"""

    with open(filepath, mode='wb') as f:
        pickler = _pickle.Pickler(f)
        pickler.dump(obj)


def upickle_from_file(filepath):
    """从文件中load对象并返回"""

    obj = {}
    if os.path.isfile(filepath):
        with open(filepath, mode='rb') as f:
            obj = _pickle.Unpickler(f)
    return obj
