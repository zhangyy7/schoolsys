#!  /usr/bin/env python
# -*- coding: utf-8 -*-
from core.course import Course
from core.schoolmember import Teacher


class Classes(object):
    """班级类"""

    def __init__(self):
        """
        param __course: 课程实例
        param __teacher: 讲师实例
        """
        self.__course = 0
        self.__teacher = 0
        self.__students = []

    @property
    def course(self, course):
        return self.__course

    @course.setter
    def course(self, course):
        if isinstance(course, Course):
            self.__course = course
        else:
            print("course必须是Course的实例！")
            return "错误码"

    @property
    def teacher(self):
        return self.__teacher

    @teacher.setter
    def teacher(self, teacher):
        if isinstance(teacher, Teacher) and teacher.course == self.course:
            self.__teacher = teacher
        else:
            print("teacher must is a instance of a %s Teacher" %
                  self.course.name)
            return "错误码"

    def add_student(self, student, caller):
        """添加学生到班级"""
        if caller == self.teacher and student not in self.students:
            self.students.append(student)
        else:
            print("您不是本班的老师或者该学生已经是本班的一员了！")
            return "错误码"
