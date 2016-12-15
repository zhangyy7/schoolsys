#! /usr/bin/env python
# -*- coding: utf8 -*-
from core import classes as cla
from core import schoolmember as sm
from settings import DATABASE
from util import pickle_to_file, upickle_from_file


class StudentView(sm.Student):
    """学员视图"""

    views = "1.注册   2.交费   3.选班级"

    def _query_course(self, school_obj):
        """查询学校已经开设的课程"""
        cou_path = DATABASE["engineer"]["file"]["course"]
        course_dict = upickle_from_file(cou_path)
        course_info_list = []
        for index, course_name in enumerate(course_dict, 1):
            single_course_tuple = ('{}.'.format(index),
                                   '课程：{}'.format(course_name),
                                   '周期：{}'.format(course_dict[course_name].cycle),
                                   '价格：{}'.format(course_dict[course_name].price))
            single_course_info = ''.join(single_course_tuple)
            course_info_list.append(single_course_info)
        return course_info_list, course_dict

    def enroll(self):
        """学员注册接口，这个注册是选学校和课程的意思，并不是register"""
        pass



class TeacherView(sm.Teacher, cla.Classes):
    pass


class AdminView(sm.School):
    pass


def get_obj(choice):
    """根据用户选择返回相应的类"""

    route = {
        "1": sm.Student,
        "2": sm.Teacher,
        "3": sm.School
    }

    return route.get(choice, False)

def
