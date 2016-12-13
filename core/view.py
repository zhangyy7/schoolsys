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
