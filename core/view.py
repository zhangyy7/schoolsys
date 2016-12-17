#! /usr/bin/env python
# -*- coding: utf8 -*-
from core import classes as cla
from core import schoolmember as sm
from settings import DATABASE
from util import pickle_to_file, upickle_from_file


class StudentView(sm.Student):
    """学员视图"""

    views = "1.注册   2.交费   3.选班级"

    @staticmethod
    def _query_course(school_obj):
        """查询学校已经开设的课程，返回str和dict形式"""

        cou_path = DATABASE["engineer"]["file"]["course"]
        course_dict = upickle_from_file(cou_path)

        course_info_list = []

        for index, course_name in enumerate(course_dict, 1):
            single_course_tuple = (
                '{num}.课程：{name}'.format(num=index, name=course_name),
                '周期：{}'.format(course_dict[course_name].cycle),
                '价格：{}'.format(course_dict[course_name].price)
            )
            single_course_info = '\t'.join(single_course_tuple)
            course_info_list.append(single_course_info)

        course_info = '\n'.join(course_info_list)
        return course_info, course_dict

    @staticmethod
    def _query_school():
        """查询学校信息，返回str形式和字典形式"""

        school_path = DATABASE["engineer"]["file"]["school"]
        school_dict = upickle_from_file(school_path)

        school_info_list = []
        for index, school in enumerate(school_dict):
            single_school_tuple = (
                '{num}.学校名称：{name}'.format(num=index, name=school.name),
                '归属地：{}'.format(school.location)
            )
            single_school_info = '\t'.join(single_school_tuple)
            school_info_list.append(single_school_info)

        school_info = '\n'.join(school_info_list)
        return school_info, school_dict

    def enroll(self):
        """学员注册接口，这个注册是选学校和课程的意思，并不是register"""
        school_info, school_dict = self._query_school()

        myschool = 0
        while not myschool:
            choice_school_num = input(
                '以下是学校信息，请选择您要报名哪所学校：\n{}'.format(school_info)
            )
            myschool = school_dict.get(choice_school_num, 0)

        choice_school_info = '您选择了学校{name}，\
                              归属地为{local}'.format(name=myschool.name,
                                                  local=myschool.location)
        print(choice_school_info)

        course_info, course_dict = self._query_course(myschool)
        mycourse = 0
        while not mycourse:
            choice_course_num = input(
                '以下是课程信息，请选择您要学习哪个课程：\n{}'.format(course_info)
            )
            mycourse = course_dict.get(choice_course_num, 0)

        choice_course_info = '您选择了课程{course_name}，\
                              周期为{cycle}，\
                              价格为{price}'.format(course_name=mycourse.name,
                                                 cycle=mycourse.cycle,
                                                 price=mycourse.price
                                                 )
        super(StudentView, self).enroll(
            myschool, mycourse)  # 调用父类的注册方法，完成学员与学校、课程的绑定

    def pay_tuition(self):
        """交学费接口"""
        issuccess = 0
        while not issuccess:
            tuition = input('您报名的课程学费为{}，请输入金额进行缴费：'.format(self.course.price))
            try:
                issuccess = super(StudentView, self).pay_tuition(tuition)
            except ValueError as e:
                print('请输入正确的金额！')


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
