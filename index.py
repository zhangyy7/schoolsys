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
    t_alex = school_beijing.create_teacher('alex', 28, 'M', python, 50000)
    classes1 = school_beijing.create_classes(python, t_alex)
    # t_alex.
    print(school_beijing.__dict__)
    print(school_shanghai.__dict__)
    print(golang.__dict__)
    print(python.__dict__)
    print(linux.__dict__)
    print(t_alex.__dict__)
    print(classes1.__dict__)


# print(__file__)
main()
