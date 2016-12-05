#!  /usr/bin/env python
# -*- coding: utf-8 -*-


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
        price_rangenge = {
            "Python": {"max": 52, "min": 24},
            "Linux": {"max": 36, "min": 12},
            "Go": {"max": 52, "min": 24}
        }
        if weeks < price_rangenge[self.name]["min"]:
            print("这么短的时间爱因斯坦也学不会啊")
        elif weeks > price_rangenge[self.name]["max"]:
            print("学习周期太长了，招不到学生学校今年的开支你包了！")
        else:
            self.__cycle = weeks

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, amount):
        price_range = {
            "Python": {"max": 24000, "min": 6500},
            "Linux": {"max": 18000, "min": 4000},
            "Go": {"max": 26000, "min": 5500}
        }
        if amount < price_range[self.name]["min"]:
            print("太便宜了，没利润喝西北风去啊！")
        elif amount > price_range[self.name]["max"]:
            print("太贵了，招不到学生学校今年的开支你包了！")
        else:
            self.__price = amount
