#! /usr/bin/env python
# -*- coding: utf-8 -*-
from core import schoolmember as ism


def main():
    """程序入口"""

    school_shanghai = ism.School("oldboyedu", "shanghai")
    school_beijing = ism.School('oldboyedu', 'beijing')
    golang = school_shanghai.create_course('Golang', 36, 15000)
    python = school_beijing.create_course('Python', 52, 19000)
    linux = school_beijing.create_course('Linux', 24, 8000)


# print(__file__)
main()
