#! /usr/bin/env python
# -*- coding: utf8 -*-
from core import classes as cla
from core import schoolmember as sm


class StudentView(sm.Student):
    views = "1.注册   2.交费   3.选班级"


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
