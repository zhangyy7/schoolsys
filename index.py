#! /usr/bin/env python
# -*- coding: utf-8 -*-
from core import schoolmember as ism
from settings import DATABASE
from util import pickle_to_file, upickle_from_file


def main():
    """程序入口"""

    # school_shanghai = ism.School("oldboyedu", "shanghai")
    school_beijing = ism.School('oldboyedu', 'beijing')
    # golang = school_shanghai.create_course('Golang', 36, 15000)
    python = school_beijing.create_course('Python', 52, 19000)
    # linux = school_beijing.create_course('Linux', 24, 8000)
    t_alex = school_beijing.create_teacher('alex', 28, 'M', python, 50000)
    classes1 = school_beijing.create_classes(python, t_alex)
    t_alex.classes = classes1
    s1 = ism.Student('kandaoge', 18, 'M')
    s1.enroll(school_beijing, python)
    s1.pay_tuition()
    students = []
    students.append(s1)
    t_alex.add_students(students)
    # print(s1.classes)
    print(classes1.students)
    classes1.add_student(s1, t_alex)


def _query_course():
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


if __name__ == '__main__':
    course_info_list, course_dict = _query_course()
    for course_info in course_info_list:
        print(course_info)

    # # classes.Classes("sss")
