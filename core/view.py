#! /usr/bin/env python
# -*- coding: utf8 -*-
import logging.config
from core import schoolmember as sm
from settings import DATABASE, LOGGING_DIC
from util import pickle_to_file, upickle_from_file


logging.config.dictConfig(LOGGING_DIC)
logger = logging.getLogger(__name__)


class BaseView(object):
    """视图基类"""

    def __init__(self):
        self.stu_path = DATABASE["engineer"]["file"]["student"]
        self.teacher_path = DATABASE["engineer"]["file"]["teacher"]
        self.school_path = DATABASE["engineer"]["file"]["school"]
        self.course_path = DATABASE["engineer"]["file"]["course"]
        self.classes_path = DATABASE["engineer"]["file"]["classes"]
        self.islogin = 0

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

    def _query_teacher(self, course_obj):
        """查询讲师信息"""
        teacher_dict = upickle_from_file(self.teacher_path)
        teacher_info_list = []
        for num, teacher in teacher_dict:
            if teacher.course == course_obj:
                single_teacher_tuple = (
                    "讲师编号：{}".format(num),
                    "讲师姓名：{}".format(teacher.name),
                    "所授课程：{}".format(teacher.course.name)
                )
                single_teacher_info = '\t'.join(single_teacher_tuple)
                teacher_info_list.append(single_teacher_info)
        teacher_info = '\n'.join(teacher_info_list)
        return teacher_info, teacher_dict

    def login(self, account_type, name):
        """"登陆方法"""
        account_type_route = {
            "1": self.student_path,
            "2": self.teacher_path,
            "3": self.school_path
        }
        obj_path = account_type_route.get(account_type, 0)
        if obj_path == 0:
            raise ValueError('account_type not exists')
        obj_dict = upickle_from_file(obj_path)
        for obj_num, obj in obj_dict.items():
            if obj.name == name:
                self.islogin = 1
                return obj
        else:
            raise ValueError('the username is not exist')


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
        logger.debug("new student [{}] is registing".format(stu_name))
        return self.stu

    def login(self, name):
        logger.debug('a student start login')
        try:
            self.stu = super(StudentView, self).login("1", name)
            logger.debug('success login')
        except ValueError as e:
            logger.error(e)

    def register_or_login(self):
        """封装register和login两个方法"""
        act = {
            "1": self.login,
            "2": self.register
        }
        act_num = input("1.登录已有账号\n2.注册新账号")
        get_act = act.get(act_num, 0)
        if get_act == 0:
            raise ValueError('action is not exist!')
        get_act()

    def enroll(self):
        """学员注册接口，这个注册是选学校和课程的意思，并不是register"""
        logger.debug('new student start enroll')
        if not self.stu:
            self.register()
        school_info, school_dict = self._query_school()
        self.stu_dict = upickle_from_file(self.stu_path)
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
            logger.debug(choice_school_info)

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
            logger.debug(choice_course_info)
            try:
                issuccess = self.stu.enroll(myschool, mycourse)
                self.stu_dict[self.stu.stu_no] = self.stu
                pickle_to_file(self.stu_path, self.stu_dict)
                logger.debug('the student enrolled finish')
            except AssertionError as e:
                logger.error(e)

    def pay_tuition(self):
        """交学费接口"""
        logger.debug('{} is starting pay tuition'.format(self.stu.name))
        issuccess = 0
        while not issuccess:
            tuition = input('您报名的课程学费为{}，请输入金额进行缴费：'.format(
                self.stu.course.price))
            try:
                issuccess = self.stu.pay_tuition(tuition)
                stu_dict = upickle_from_file(self.stu_path)
                stu_dict[self.stu.num] = self.stu
                pickle_to_file(self.stu_path, stu_dict)
                logger.debug(
                    'the student {} finished pay'.format(self.stu.name))
            except ValueError as e:
                print('请输入正确的金额！')
                logger.error(e)

    def choice_classes(self):
        """选班级"""
        logger.debug(
            'the student {} is starting choice classes'.format(self.stu.name))
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
                logger.debug('student {} finished choice classes[{}]'.format(
                    self.stu.name, self.stu.classes.name))
            except AssertionError as e:
                logger.error(e)
            except ValueError as e:
                logger.error(e)


class TeacherView(BaseView):
    """讲师视图"""

    def __init__(self):
        super(TeacherView, self).__init__()
        self.teacher = 0

    def teaching(self):
        """上课接口"""
        classes_info, classes_dict = self._query_classes()


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
        logger.debug('school {} created'.format(school_obj.name))
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
        logger.debug('start create course')
        _, course_dict = self._query_course(school_obj)
        course_obj = 0
        while not course_obj:
            try:
                course_name = input("请输入课程名称：").strip().capitalize()
                course_cycle = input("请输入课程周期：")
                course_price = input("请输入课程价格：")
                course_obj = school_obj.create_course(
                    course_name, course_cycle, course_price)
                logger.debug(
                    'course {} created finish'.format(course_obj.name))
            except ValueError as e:
                logger.error(e)

    def create_classes(self):
        """创建班级接口"""
        logger.debug('starting create classes')
        school_info, school_dict = self._query_school()

        myschool = 0
        while not myschool:
            school_num = input("以下是学校信息，请选择为哪所学校创建班级".format(school_info))
            myschool = school_dict.get(school_num, 0)

        course_info, course_dict = self._query_course(myschool)
        mycourse = 0
        while not mycourse:
            course_num = input("该校区已开课程如下，请选择：\n{}".format(course_info))
            mycourse = course_dict.get(course_num, 0)
            if mycourse == 0:
                print("您输入的不正确，请重新选择")

        teacher_info, teacher_dict = self._query_teacher(mycourse)
        myteacher = 0
        while not myteacher:
            teacher_num = input("以下是课程{}的讲师信息，请选择：\n{}".format(
                mycourse.name, teacher_info
            ))
            myteacher = teacher_dict.get(teacher_num, 0)
            if myteacher == 0:
                print("输入错误，请重新选择！")
        try:
            classes_obj = myschool.create_classes(mycourse, myteacher)
            logger.debug('create classes[{}] end'.format(classes_obj.name))
            return classes_obj
        except Exception as e:
            logger.error(e)


def get_obj(choice):
    """根据用户选择返回相应的类"""

    route = {
        "1": sm.Student,
        "2": sm.Teacher,
        "3": sm.School
    }

    return route.get(choice, False)
