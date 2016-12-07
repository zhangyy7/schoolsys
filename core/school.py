#! /usr/bin/env pytohn
# -*-coding: utf-8 -*-
from core.course import Course
from core.schoolmember import Teacher
from core.classes import Classes


class School(object):
    """学校基类"""

    def __init__(self, schoolname, location):
        """
        param name: 学校名称
        param location: 学校所在城市
        """
        self.schoolname = schoolname
        self.location = location

    def create_classes(self, course, teacher):
        """创建班级，没有具体实现，要求子类（学校管理员）必须实现此方法"""
        classes = Classes()
        classes.course = course
        classes.teacher = teacher

    def create_course(self, course_name, cycle, price):
        """创建课程，没有具体实现，要求子类（学校管理员）必须实现此方法"""
        course = Course(course_name)
        course.cycle = cycle
        course.price = price

    def create_teacher(self):
        """创建讲师，没有具体实现，要求子类（学校管理员）必须实现此方法"""
        pass
