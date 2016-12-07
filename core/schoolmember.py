#! /usr/bin/env python
# -*-coding: utf-8 -*-
from core import classes
from settings import COURSES


class School(object):
    """学校类"""

    def __init__(self, schoolname, location):
        """
        param name: 学校名称
        param location: 学校所在城市
        """
        self.schoolname = schoolname
        self.location = location

    def create_classes(self, course, teacher):
        """创建班级，没有具体实现，要求子类（学校管理员）必须实现此方法"""
        clas_obj = classes.Classes()
        clas_obj.course = course
        clas_obj.teacher = teacher

    def create_course(self, course_name, cycle, price):
        """创建课程，没有具体实现，要求子类（学校管理员）必须实现此方法"""
        course_obj = Course(self, course_name)
        course_obj.cycle = cycle
        course_obj.price = price
        return course_obj

    def create_teacher(self, name, age, sex, school, course, salary):
        """创建讲师，没有具体实现，要求子类（学校管理员）必须实现此方法"""


class Course(object):
    """课程类"""

    def __init__(self, creator, name):
        # print(isinstance(creator, School))
        if isinstance(creator, School) and creator.location in COURSES[name]["location"]:
            self.name = name
            self.__cycle = 0
            self.__price = 0
        else:
            raise NameError("不能实例化我")

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


class SchoolMember(object):
    """学校成员基类，定义学校成员通用的基本属性"""

    member = 0

    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

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

    def enroll(self, course, amount):
        super(Teacher, self).enroll()
        self.__salary = 0  # 构造对象时默认为0，后续通过setter方法进行赋值
        if isinstance(course, Course):
            self.course = course
        else:
            print("只能传入课程")
            return "错误码"
        self.salary = amount

    def __set_salary(self, amount):
        """判断薪水范围"""

        amount = int(amount)
        if amount > COURSES[self.course.name]["salary"]["max"]:
            print("%s 讲师的薪水上限为%d,你咋不上天呢！" %
                  (self.course.name, COURSES[self.course.name]["salary"]["max"]))
        elif amount < COURSES[self.course.name]["salary"]["min"]:
            print("%s 讲师的薪水最少也得%d,你打发要饭的呢！" %
                  (self.course.name, COURSES[self.course.name]["salary"]["min"]))
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


class Student(SchoolMember):
    """学生类，继承自学校成员类"""

    def enroll(self, school, course):
        super(Student, self).enroll()
        if isinstance(school, School) and isinstance(course, Course):
            self.school = school
            self.courses = {}
            self.courses[course] = {}
            self.courses[course]["ispaied"] = False

        else:
            print("请选择正确的学校和课程")

    # def pay_tuition(self):
    #     """交学费方法"""
    #     self.total_tuition += self.course.price
    #     self.
