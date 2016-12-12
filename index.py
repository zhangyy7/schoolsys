#! /usr/bin/env python
# -*- coding: utf-8 -*-
from core import schoolmember as ism
from core import classes


def main():
    """程序入口"""

    school_shanghai = ism.School("oldboyedu", "shanghai")
    school_beijing = ism.School('oldboyedu', 'beijing')
    golang = school_shanghai.create_course('Golang', 36, 15000)
    python = school_beijing.create_course('Python', 52, 19000)
    linux = school_beijing.create_course('Linux', 24, 8000)
    t_alex = school_beijing.create_teacher('alex', 28, 'M', python, 50000)
    classes1 = school_beijing.create_classes(python, t_alex)
    t_alex.classes = classes1
    s1 = ism.Student('kandaoge', 18, 'M')
    s1.enroll(school_beijing, python)
    students = []
    students.append(s1)
    t_alex.add_students(students)
    print(s1.classes)
    print(classes1.students)
    t_alex.remove_students(students)
    print(s1.classes)
    print(classes1.students)
    s1.score = 101
    print(s1.score)

# print(__file__)

if __name__ == '__main__':
    main()
    # classes.Classes("sss")
