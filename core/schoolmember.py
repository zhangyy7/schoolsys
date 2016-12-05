#! /usr/bin/env python
# -*-coding: utf-8 -*-


class SchoolMember(object):
    """学校成员基类，定义学校成员通用的基本属性"""

    member = 0

    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
        self.enroll()

    def enroll(self):
        SchoolMember.member += 1

    def __str__(self):
        """返回实例的所有属性"""
        info = ""
        for k, v in self.__dict__.items():
            info += "%s: %s\n" % (k, v)
        return "=====info=====\n%s=====end=====" % info

    __repr__ = __str__


class Teacher(SchoolMember):
    """讲师类，学校成员的一个子类"""

    def __init__(self, name, age, sex, course):
        super(Teacher, self).__init__(name, age, sex)
        self.course = course
        self.__salary = 0  # 构造对象时默认为0，后续通过setter方法进行赋值

    def __set_salary(self, amount):
        """判断薪水范围"""

        amount = int(amount)
        salary_range = {
            "Python": {"max": 50000, "min": 18000},
            "Linux": {"max": 60000, "min": 15000},
            "Go": {"max": 65000, "min": 20000}
        }
        if amount > salary_range[self.course.name]["max"]:
            print("%s 讲师的薪水上限为%d,你咋不上天呢！" %
                  (self.course.name, salary_range[self.course.name]["max"]))
        elif amount < salary_range[self.course.name]["min"]:
            print("%s 讲师的薪水最少也得%d,你打发要饭的呢！" %
                  (self.course.name, salary_range[self.course.name]["min"]))
        else:
            self.__salary = amount

    @property
    def salary(self):  # 私有属性__salery
        return self.__salary

    @salary.setter
    def salary(self, amount):
        """
        给私有变量__salery赋值，在这可以对amount的值做各种限制和判断
        在调用的时候形式上却和普通赋值并无二致，好评！
        """
        self.__set_salary(amount)
