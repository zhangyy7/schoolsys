#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging.config
from core import schoolmember as csm
from settings import CLASSES_MAX_STUDENTS as cms
from settings import LOGGING_DIC, DATABASE
from util import pickle_to_file, upickle_from_file


logging.config.dictConfig(LOGGING_DIC)
logger = logging.getLogger(__name__)


class Classes(object):
    """班级类"""

    classes_num = 0

    def __init__(self, school_obj):
        """
        班级实例只能由学校实例创建，实例化之后与创建者绑定，且不能修改
        成功实例化之后需要设置其他属性：
        __course 必须是课程实例
        __teacher 必须是讲师实例
        __students 为学员列表，列表的每个元素都必须是学生实例
        __max_students 为班级可容纳的最大学生数量，默认值在settings里设置
        """
        # print("classes.__init__", isinstance(school_obj, csm.School))
        # print(self)
        self.__school = school_obj
        self.name = 0
        self.__course = 0
        self.__teacher = 0
        self.__students = []
        self.__max_students = cms
        self.mypath = DATABASE["engineer"]["file"]["classes"]
        self.num = Classes.classes_num + 1
        Classes.classes_num += 1
        classes_dict = upickle_from_file(self.mypath)
        classes_dict[str(self.num)] = self
        pickle_to_file(self.mypath, classes_dict)


# 已下property装饰的函数都是访问或设置构造方法中的私有变量的唯一接口
    @property
    def school(self):
        return self.__school

    @school.setter
    def school(self, school_obj):
        assert isinstance(school_obj, csm.School), 'value only a school'
        self.__school = school_obj

    @property
    def course(self):
        return self.__course

    @course.setter
    def course(self, course):
        assert isinstance(
            course, csm.Course), 'course must be a instance of Course'
        self.__course = course
        self.name = "{c_name}-{num}班".format(
            c_name=self.course.name, num=self.num)

    @property
    def teacher(self):
        return self.__teacher

    @teacher.setter
    def teacher(self, teacher):
        """
        设置班级的老师
        :param teacher: 老师类的实例
        当teacher不是老师类的实例的时候抛异常
        当teacher的课程与本班级的课程不一致时抛异常
        """
        msg = 'teacher must is a instance of a {} Teacher'.format(
            self.course.name)
        assert isinstance(teacher, csm.Teacher), msg
        assert teacher.course == self.course, msg
        self.__teacher = teacher

    @property
    def students(self):
        return self.__students

    @property
    def max_students(self):
        return self.__max_students

    @max_students.setter
    def max_students(self, qty):
        """设置班级容纳学生的最大数量"""
        if qty.isdigit() and int(qty) < cms:
            self.__max_students = int(qty)
        else:
            raise ValueError('班级所能容纳的最大学生数量只能是数字并且小于%s' % cms)

    def add_student(self, student, caller):
        """添加学生到班级，只有本班的老师可以操作"""
        assert caller == self.teacher, 'you not is a teacher of this Classes'
        if student not in self.students:
            self.__students.append(student)
        else:
            raise KeyError('the student already exists')

    def remove_student(self, student, caller):
        """从班级里移除学生，只有本班老师可以操作"""
        if caller == self.teacher and student in self.__students:
            self.__students.remove(student)
        else:
            raise ValueError('您不是本班老师或者该学生不是本班学员')
