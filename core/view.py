#! /usr/bin/env python
# -*- coding: utf8 -*-
from core import classes as cla
from core import schoolmember as sm
from settings import DATABASE
from util import pickle_to_file, upickle_from_file


class BaseView(object):
    """视图基类"""

    @staticmethod
    def _query_course(school_obj):
        """查询学校已经开设的课程，返回str和dict形式"""

        cou_path = DATABASE["engineer"]["file"]["course"]
        course_dict = upickle_from_file(cou_path)

        course_info_list = []

        for index, course_num in enumerate(course_dict, 1):
            single_course_tuple = (
                '{num}.课程编号：{course_num}'.format(
                    num=index, course_num=course_num),
                '课程名称：{}'.format(course_dict[course_num].name),
                '周期：{}'.format(course_dict[course_num].cycle),
                '价格：{}'.format(course_dict[course_num].price)
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
        print(school_dict)
        # if not school_dict:
        #     print("不存在学校，请联系管理员！")
        #     return
        school_info_list = []
        for index, school in enumerate(school_dict):
            single_school_tuple = (
                '{num}.学校名称：{name}'.format(num=index, name=school.name),
                '归属地：{}'.format(school.location)
            )
            single_school_info = '\t'.join(single_school_tuple)
            print(single_school_info)
            print(single_school_tuple)
            school_info_list.append(single_school_info)

        school_info = '\n'.join(school_info_list)
        return school_info, school_dict

    @staticmethod
    def _query_classes(course_obj):
        """查询班级数据"""
        cla_path = DATABASE["engineer"]["file"]["classes"]
        classes_dict = upickle_from_file(cla_path)

        classes_info_list = []
        for index, cla_num in enumerate(classes_dict, 1):
            if course_obj.name == classes_dict[cla_num].name:
                single_classes_tuple = (
                    "{num}.课程编号：{cla_num}".format(
                        num=index, cla_num=cla_num),
                    "课程名称：{}".format(classes_dict[cla_num].name),
                    "班级总人数：{}".format(classes_dict[cla_num].max_students),
                    "已报名人数：{}".format(len(classes_dict[cla_num].students))
                )
                single_classes_info = '\t'.join(single_classes_tuple)
                classes_info_list.append(single_classes_info)

        classes_info = '\n'.join(classes_info_list)
        return classes_info, classes_dict


class StudentView(sm.Student, BaseView):
    """学员视图"""

    views = "1.注册   2.交费   3.选班级"

    def enroll(self):
        """学员注册接口，这个注册是选学校和课程的意思，并不是register"""
        school_info, school_dict = self._query_school()
        # print(school_info)
        issuccess = 0
        while not issuccess:
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
            print(choice_course_info)

            issuccess = super(StudentView, self).enroll(
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

    def choice_classes(self):
        """选班级"""
        classes_info, classes_dict = self._query_classes()

        issuccess = 0
        while not issuccess:
            myclasses = 0
            while not myclasses:
                choice_cla_num = input('班级信息如下，请选择：\n{}'.format(classes_info))
                myclasses = classes_dict.get(choice_cla_num, 0)
            choice_cla_info = "您选择了班级{name}".format(myclasses.name)
            print(choice_cla_info)
            try:
                self.classes = myclasses
                issuccess = 1
            except AssertionError as e:
                print(e)
            except ValueError as e:
                print(e)


class TeacherView(sm.Teacher, BaseView):
    pass


class AdminView(sm.School, BaseView):
    pass


def get_obj(choice):
    """根据用户选择返回相应的类"""

    route = {
        "1": sm.Student,
        "2": sm.Teacher,
        "3": sm.School
    }

    return route.get(choice, False)
