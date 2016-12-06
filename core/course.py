#!  /usr/bin/env python
# -*- coding: utf-8 -*-
from setting import COURSES


class Course(object):
    """课程类"""

    def __init__(self, name):
        self.name = name
        self.__cycle = 0
        self.__price = 0

    def __str__(self):
        """返回实例的所有属性"""
        info = ""
        for k, v in self.__dict__.items():
            info += "%s: %s\n" % (k, v)
        return "=====info=====\n%s=====end=====" % info

    @property
    def cycle(self):
        return self.__cycle

    @cycle.setter
    def cycle(self, weeks):
        if weeks < COURSES[self.name]["cycle"]["min"]:
            print("这么短的时间爱因斯坦也学不会啊")
        elif weeks > COURSES[self.name]["cycle"]["max"]:
            print("学习周期太长了，招不到学生学校今年的开支你包了！")
        else:
            self.__cycle = weeks

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, amount):
        if amount < COURSES[self.name]["price"]["min"]:
            print("太便宜了，没利润喝西北风去啊！")
        elif amount > COURSES[self.name]["price"]["max"]:
            print("太贵了，招不到学生学校今年的开支你包了！")
        else:
            self.__price = amount
