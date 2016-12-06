#!  /usr/bin/env python
# -*- coding: utf-8 -*-


class Classes(object):
    """班级类"""

    def __init__(self, course, teacher):
        """
        param course: 课程实例
        param teacher: 讲师实例
        """
        self.course = course
        self.teacher = teacher
        self.students = []

    def add_student(self, student, caller):
        """添加学生到班级"""
        if caller == self.teacher and student not in self.students:
            self.students.append(student)
        else:
            print("您不是本班的老师或者该学生已经是本班的一员了！")
            return "错误码"
