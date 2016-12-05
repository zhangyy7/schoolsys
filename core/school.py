#! /usr/bin/env pytohn
# -*-coding: utf-8 -*-


class School(object):
    """学校基类"""

    def __init__(self, name, location):
        """
        param name: 学校名称
        param location: 学校所在城市
        """
        self.name = name
        self.location = location

    def create_classes(self, Course, Teacher):
        """创建班级，没有具体实现，要求子类（学校管理员）必须实现此方法"""
        pass

    def create_course(self, Course):
        """创建课程，没有具体实现，要求子类（学校管理员）必须实现此方法"""
        pass

    def create_teacher(self, Teacher):
        """创建讲师，没有具体实现，要求子类（学校管理员）必须实现此方法"""
        pass
