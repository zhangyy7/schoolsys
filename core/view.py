#! /usr/bin/env python
# -*- coding: utf8 -*-
from core import classes as cla
from core import schoolmember as sm
from settings import DATABASE
from util import pickle_to_file, upickle_from_file


class BaseView(object):
    """视图基类"""

    def __init__(self):
        self.stu_path = DATABASE["engineer"]["file"]["student"]
        self.teacher_path = DATABASE["engineer"]["file"]["teacher"]
        self.school_path = DATABASE["engineer"]["file"]["school"]
        self.course_path = DATABASE["engineer"]["file"]["course"]
        self.classes_path = DATABASE["engineer"]["file"]["classes"]

    def _query_course(self, school_obj):
        """查询学校已经开设的课程，返回str和dict形式"""

        course_dict = upickle_from_file(self.course_path)

        course_info_list = []

        for index, course_num in enumerate(course_dict, 1):
            if course_dict[course_num].school == school_obj:
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

    def _query_school(self):
        """查询学校信息，返回str形式和字典形式"""

        school_dict = upickle_from_file(self.school_path)
        print(school_dict)
        school_info_list = []
        for index, school_num in enumerate(school_dict, 1):
            single_school_tuple = (
                '{num}.学校编号：{school_num}'.format(
                    num=index, school_num=school_num),
                '学校名称：{name}'.format(
                    num=index, name=school_dict[school_num].name
                ),
                '归属地：{}'.format(school_dict[school_num].location)
            )
            single_school_info = '\t'.join(single_school_tuple)
            school_info_list.append(single_school_info)

        school_info = '\n'.join(school_info_list)
        return school_info, school_dict

    def _query_classes(self, course_obj):
        """查询班级数据"""
        classes_dict = upickle_from_file(self.classes_path)

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


class StudentView(BaseView):
    """学员视图"""

    views = "1.注册   2.交费   3.选班级"

    def __init__(self):
        super(StudentView, self).__init__()
        self.stu = 0

    def register(self):
        """学生注册学校账号"""
        if self.stu:
            return self.stu
        stu_dict = upickle_from_file(self.stu_path)
        stu_name = input("请输入您的姓名：")
        stu_age = input("请输入您的年龄：")
        stu_sex = input("请输入您的性别：")
        self.stu = sm.Student(stu_name, stu_age, stu_sex)
        stu_dict[self.stu.stu_no] = self.stu
        pickle_to_file(self.stu_path, stu_dict)
        # return self.stu

    def enroll(self):
        """学员注册接口，这个注册是选学校和课程的意思，并不是register"""
        if not self.stu:
            self.register()
        school_info, school_dict = self._query_school()
        self.stu_dict = upickle_from_file(self.stu_path)
        # print(school_info)
        if not school_info:
            print("学校还没成立，联系管理员或稍后再来！")
            return
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
                   price=mycourse.price)
            print(choice_course_info)
            try:
                issuccess = self.stu.enroll(myschool, mycourse)
                self.stu_dict[self.stu.stu_no] = self.stu
                pickle_to_file(self.stu_path, self.stu_dict)
            except AssertionError as e:
                print(e)

    def pay_tuition(self):
        """交学费接口"""
        issuccess = 0
        while not issuccess:
            tuition = input('您报名的课程学费为{}，请输入金额进行缴费：'.format(
                self.stu.course.price))
            try:
                issuccess = self.stu.pay_tuition(tuition)
                stu_dict = upickle_from_file(self.stu_path)
                stu_dict[self.stu.num] = self.stu
                pickle_to_file(self.stu_path, stu_dict)
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


class AdminView(BaseView):
    """管理视图"""

    def create_school(self):
        """创建学校"""
        school_name = input("请输入学校名称：")
        school_location = input("请输入学校位置：")
        school_obj = sm.School(school_name, school_location)
        _, school_dict = self._query_school()
        school_dict[str(school_obj.num)] = school_obj
        pickle_to_file(self.school_path, school_dict)
        return school_obj

    def create_teacher(self, school_obj):
        """创建讲师"""
        teacher_name = input("请输入讲师姓名：")
        teacher_age = input("请输入讲师年龄：")
        teacher_sex = input("请输入讲师性别：")
        course_info, course_dict = self._query_course()
        teacher_course = 0
        while not teacher_course:
            teacher_course_num = input(
                "请从以下课程列表里选择讲师的课程：\n{}".format(course_info)
            )
            teacher_course = course_dict.get(teacher_course_num, 0)
        teacher_salary = input("请输入讲师工资：")
        teacher_obj = school_obj.create_teacher(
            teacher_name,
            teacher_age,
            teacher_sex,
            teacher_course,
            teacher_salary
        )
        return teacher_obj

    def create_course(self, school_obj):
        """创建课程"""
        _, course_dict = self._query_course(school_obj)
        course_obj = 0
        while not course_obj:
            try:
                course_name = input("请输入课程名称：").strip().capitalize()
                course_cycle = input("请输入课程周期：")
                course_price = input("请输入课程价格：")
                course_obj = school_obj.create_course(
                    course_name, course_cycle, course_price)
            except ValueError as e:
                print(e)


def get_obj(choice):
    """根据用户选择返回相应的类"""

    route = {
        "1": sm.Student,
        "2": sm.Teacher,
        "3": sm.School
    }

    return route.get(choice, False)
