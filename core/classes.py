#! /usr/bin/env python
# -*- coding: utf-8 -*-
from core import schoolmember as csm
from settings import CLASSES_MAX_STUDENTS as cms


class Classes(object):
    """班级类"""

    def __init__(self, school_obj):
        """
        班级实例只能由学校实例创建，实例化之后与创建者绑定，且不能修改
        成功实例化之后需要设置其他属性：
        __course 必须是课程实例
        __teacher 必须是讲师实例
        __students 为学员列表，列表的每个元素都必须是学生实例
        __max_students 为班级可容纳的最大学生数量，默认值在settings里设置
        """
        if isinstance(school_obj, csm.School):
            self.__school = school_obj
            self.__course = 0
            self.__teacher = 0
            self.__students = []
            self.__max_students = cms
        else:
            raise TypeError('creator must be a instance of School')

# 已下property装饰的函数都是访问或设置构造方法中的私有变量的唯一接口
    @property
    def school(self):
        return self.__school

    @property
    def course(self, course):
        return self.__course

    @course.setter
    def course(self, course):
        if isinstance(course, csm.Course):
            self.__course = course
        else:
            print("course必须是Course的实例！")
            return "错误码"

    @property
    def teacher(self):
        return self.__teacher

    @teacher.setter
    def teacher(self, teacher):
        if isinstance(teacher, csm.Teacher) and teacher.course == self.course:
            self.__teacher = teacher
        else:
            print("teacher must is a instance of a %s Teacher" %
                  self.course.name)
            return "错误码"

    @property
    def students(self):
        return self.__students

    @property
    def max_students(self):
        return self.__max_students

    @max_students.setter
    def max_students(self, qty):
        if qty.isdigit() and qty < cms:
            self.__max_students = qty
        else:
            raise ValueError('班级所能容纳的最大学生数量只能是数字并且小于%s' % cms)

    def add_student(self, student, caller):
        """添加学生到班级，只有本班的老师可以操作"""
        if caller == self.teacher and student not in self.students:
            self.__students.append(student)
        else:
            print("您不是本班的老师或者该学生已经是本班的一员了！")
            return "错误码"

    def remove_student(self, student, caller):
        """从班级里移除学生，只有本班老师可以操作"""
        if caller == self.teacher and student in self.__students:
            self.__students.remove(student)
        else:
            raise ValueError('您不是本班老师或者该学生不是本班学员')
