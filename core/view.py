#! /usr/bin/env python
# -*- coding: utf8 -*-
from core import classes as cla
from core import schoolmember as sm


class StudentView(sm.Student):
    pass


class TeacherView(sm.Teacher):
    pass


class AdminView(sm.School):
    pass
