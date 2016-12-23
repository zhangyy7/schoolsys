#! /usr/bin/env python
# -*- coding: utf8 -*-
import logging.config

from core import schoolmember as sm
from settings import DATABASE, LOGGING_DIC
from util import auth, pickle_to_file, upickle_from_file

logging.config.dictConfig(LOGGING_DIC)
logger = logging.getLogger(__name__)


class BaseView(object):
    """视图基类"""

    def __init__(self):
        self.student_path = DATABASE["engineer"]["file"]["student"]
        self.teacher_path = DATABASE["engineer"]["file"]["teacher"]
        self.school_path = DATABASE["engineer"]["file"]["school"]
        self.course_path = DATABASE["engineer"]["file"]["course"]
        self.classes_path = DATABASE["engineer"]["file"]["classes"]
        self.islogin = 0
        self.try_count = 0

    def _query_course(self, school_obj):
        """查询学校已经开设的课程，返回str和dict形式"""

        course_dict = upickle_from_file(self.course_path)
        if not course_dict:
            raise ValueError("课程不存在，请联系管理员")

        course_info_list = []

        for index, course_num in enumerate(course_dict, 1):
            if course_dict[course_num].school == school_obj:
                single_course_tuple = (
                    '{num}.课程编号：{course_num}'.format(
                        num=index, course_num=course_num),
                    '课程名称：{}'.format(course_dict[course_num].name),
                    '周期：{}'.format(course_dict[course_num].cycle),
                    '价格：{}'.format(course_dict[course_num].price))
                single_course_info = '\t'.join(single_course_tuple)
                course_info_list.append(single_course_info)
        course_info = '\n'.join(course_info_list)
        return course_info, course_dict

    def _query_school(self):
        """查询学校信息，返回str形式和字典形式"""

        school_dict = upickle_from_file(self.school_path)
        if not school_dict:
            raise ValueError("学校不存在请联系管理员")
        school_info_list = []
        for index, school_num in enumerate(school_dict, 1):
            single_school_tuple = (
                '{num}.学校编号：{school_num}'.format(
                    num=index, school_num=school_num), '学校名称：{name}'.format(
                        num=index, name=school_dict[school_num].name),
                '归属地：{}'.format(school_dict[school_num].location))
            single_school_info = '\t'.join(single_school_tuple)
            school_info_list.append(single_school_info)

        school_info = '\n'.join(school_info_list)
        return school_info, school_dict

    def _query_classes(self, course_obj):
        """查询班级数据"""
        classes_dict = upickle_from_file(self.classes_path)
        if not classes_dict:
            raise ValueError("班级不存在请联系管理员")

        classes_info_list = []
        for index, cla_num in enumerate(classes_dict, 1):
            if course_obj.name == classes_dict[cla_num].course.name:
                single_classes_tuple = (
                    "{num}.课程编号：{cla_num}".format(
                        num=index, cla_num=cla_num),
                    "课程名称：{}".format(classes_dict[cla_num].name),
                    "班级总人数：{}".format(classes_dict[cla_num].max_students),
                    "已报名人数：{}".format(len(classes_dict[cla_num].students)))
                single_classes_info = '\t'.join(single_classes_tuple)
                classes_info_list.append(single_classes_info)
        classes_info = '\n'.join(classes_info_list)
        # print('查询班级信息：', classes_info)
        return classes_info, classes_dict

    def _query_teacher(self, course_obj):
        """查询讲师信息"""
        teacher_dict = upickle_from_file(self.teacher_path)
        if not teacher_dict:
            raise ValueError("讲师不存在，请联系管理员")

        teacher_info_list = []
        for num, teacher in teacher_dict.items():
            if teacher.course == course_obj:
                single_teacher_tuple = ("讲师编号：{}".format(num),
                                        "讲师姓名：{}".format(teacher.name),
                                        "所授课程：{}".format(teacher.course.name))
                single_teacher_info = '\t'.join(single_teacher_tuple)
                teacher_info_list.append(single_teacher_info)
        teacher_info = '\n'.join(teacher_info_list)
        print(teacher_info)
        return teacher_info, teacher_dict

    def _query_student(self, course_obj):
        student_dict = upickle_from_file(self.student_path)
        if not student_dict:
            raise ValueError("学生不存，努力招生吧！")

        student_info_list = []
        for num, student in student_dict.items():
            if student.course.name == course_obj.name:
                single_student_tuple = ("学生编号：{}".format(num),
                                        "学生姓名：{}".format(student.name),
                                        "课程：{}".format(student.course.name))
                single_teacher_info = '\t'.join(single_student_tuple)
                student_info_list.append(single_teacher_info)
        student_info = '\n'.join(student_info_list)
        return student_info, student_dict

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
        if not obj_dict:
            self.try_count += 1
            raise ValueError('accout not exists')
        for obj_num, obj in obj_dict.items():
            if obj.name == name:
                self.islogin = 1
                return obj
        else:
            self.try_count += 1
            raise ValueError('the username is not exist')


class StudentView(BaseView):
    """学员视图"""

    def __init__(self):
        super(StudentView, self).__init__()
        self.stu = 0
        self.route()

    def route(self):
        func_route = {
            "1": self.enroll,
            "2": self.pay_tuition,
            "3": self.choice_classes,
            "4": exit
        }
        while True:
            act_num = input("1.注册 2.交学费 3.选班级 4.退出程序，其他任意键退出学生视图\n>>>").strip()
            act_func = func_route.get(act_num, 0)
            if not act_func:
                break
            act_func()

    def register(self):
        """学生注册学校账号"""
        if self.stu:
            return self.stu
        stu_dict = upickle_from_file(self.student_path)
        stu_name = input("请输入您的姓名：".capitalize()).strip()
        stu_age = input("请输入您的年龄：").strip()
        stu_sex = input("请输入您的性别：").strip()
        self.stu = sm.Student(stu_name, stu_age, stu_sex)
        stu_dict[str(self.stu.stu_no)] = self.stu
        pickle_to_file(self.student_path, stu_dict)
        logger.debug("new student [{}] is registing".format(stu_name))
        return self.stu

    def login(self):
        logger.debug('a student start login')
        if not self.stu:
            while self.try_count < 3:
                stu_name = input("请输入姓名：".strip())
                try:
                    self.stu = super(StudentView, self).login("1", stu_name)
                    logger.debug('success login')
                    print("登录成功！")
                    return True
                except ValueError as e:
                    logger.error(e)
            else:
                print("次数用尽！")
                return False
        else:
            return True

    def register_or_login(self):
        if self.stu:
            return True
        """封装register和login两个方法"""
        act = {"1": self.login, "2": self.register}
        get_act = 0
        while not get_act:
            act_num = input("1.登录已有账号\n2.注册新账号\n>>>")
            get_act = act.get(act_num, 0)
            if get_act == 0:
                print("没有这个选项！")
        return get_act()

    @auth(register_or_login)
    def enroll(self):
        """学员注册接口，这个注册是选学校和课程的意思，并不是register"""
        logger.debug('new student start enroll')
        if not self.stu:
            self.register()
        school_info, school_dict = self._query_school()
        self.stu_dict = upickle_from_file(self.student_path)
        if not school_info:
            print("学校还没成立，联系管理员或稍后再来！")
            return
        issuccess = 0
        while not issuccess:
            myschool = 0
            while not myschool:
                choice_school_num = input('以下是学校信息：\n{}\n请选择您要报名哪所学校>>>'.format(
                    school_info))
                myschool = school_dict.get(choice_school_num, 0)
            choice_school_info = '您选择了学校{name}，\
                                归属地为{local}'.format(
                name=myschool.name, local=myschool.location)
            print(choice_school_info)
            logger.debug(choice_school_info)

            course_info, course_dict = self._query_course(myschool)
            mycourse = 0
            while not mycourse:
                choice_course_num = input('以下是课程信息：\n{}\n请选择您要学习哪个课程>>>'.format(
                    course_info))
                mycourse = course_dict.get(choice_course_num, 0)

            choice_course_info = '您选择了课程{course_name}，\
周期为{cycle}，\
价格为{price}'.format(
                course_name=mycourse.name,
                cycle=mycourse.cycle,
                price=mycourse.price)
            print(choice_course_info)
            logger.debug(choice_course_info)
            try:
                issuccess = self.stu.enroll(myschool, mycourse)
                self.stu_dict[self.stu.stu_no] = self.stu
                pickle_to_file(self.student_path, self.stu_dict)
                logger.debug('the student enrolled finish')
            except AssertionError as e:
                logger.error(e)

    @auth(register_or_login)
    def pay_tuition(self):
        """交学费接口"""
        logger.debug('{} is starting pay tuition'.format(self.stu.name))
        if not any((self.stu.course, self.stu.school)):  # 课程或学校有任何一个属性为假
            print("请先注册基本信息")
            return self.enroll()
        if self.stu.ispaied:
            print("您已经交过学费了，有钱也不能当冤大头啊！")
            return
        issuccess = 0
        while not issuccess:
            tuition = input('您报名的课程学费为{}，请输入金额进行缴费：'.format(
                self.stu.course.price))
            try:
                issuccess = self.stu.pay_tuition(tuition)
                stu_dict = upickle_from_file(self.student_path)
                stu_dict[str(self.stu.stu_no)] = self.stu
                pickle_to_file(self.student_path, stu_dict)
                logger.debug('the student {} finished pay'.format(
                    self.stu.name))
                print("交费成功，可以选班级开始学习了！")
            except ValueError as e:
                print('请输入正确的金额！')
                logger.error(e)

    @auth(register_or_login)
    def choice_classes(self):
        """选班级"""
        logger.debug('the student {} is starting choice classes'.format(
            self.stu.name))
        classes_info, classes_dict = self._query_classes(self.stu.course)

        issuccess = 0
        while not issuccess:
            myclasses = 0
            while not myclasses:
                choice_cla_num = input(
                    '班级信息如下：\n{}\n请选择>>>'.format(classes_info))
                myclasses = classes_dict.get(choice_cla_num, 0)
            choice_cla_info = "您选择了班级{}".format(myclasses.name)
            print(choice_cla_info)
            try:
                self.stu.classes = myclasses
                issuccess = 1
                logger.debug('student {} finished choice classes[{}]'.format(
                    self.stu.name, self.stu.classes.name))
                student_ditc = upickle_from_file(self.student_path)
                student_ditc[str(self.stu.stu_no)] = self.stu
                pickle_to_file(self.student_path, student_ditc)
            except AssertionError as e:
                logger.error(e)
            except ValueError as e:
                logger.error(e)
            except PermissionError as e:
                print(e)
                return False


class TeacherView(BaseView):
    """讲师视图"""

    def __init__(self):
        super(TeacherView, self).__init__()
        self.teacher = 0
        self.route()

    def route(self):
        func_route = {"1": self.teaching,
                      "2": self.modify_student_score,
                      "3": self.bind_classes,
                      "4": self.add_student_classes,
                      "5": exit}
        while True:
            act_num = input(
                "1.上课 2.修改学生成绩 3.绑定班级 4.添加学生入班 5.退出程序，其他任意键退出讲师视图\n>>>"
            ).strip()
            act_func = func_route.get(act_num, 0)
            if not act_func:
                break
            act_func()

    def login(self):
        if not self.teacher:
            print("请先登陆！")
            try:
                logger.debug('a teacher begin login')
                while self.try_count < 3:
                    name = input("请输入您的姓名：\n>>>").capitalize().strip()
                    try:
                        self.teacher = super(TeacherView,
                                             self).login("2", name)
                        logger.debug('teacher[{}] login success'.format(name))
                        print("登陆成功！")
                        return True
                    except ValueError as e:
                        logger.error(e)
                        self.try_count += 1
                        print("登陆失败请重试！")
                else:
                    print('too many try!')
                    return False
            except ValueError as e:
                exit(e)
        else:
            return True

    @auth(login)
    def bind_classes(self):
        """绑定班级"""
        classes_info, classes_dict = self._query_classes(self.teacher.course)
        if not classes_info:
            raise ValueError("您所授课程还没有班级，请联系管理员！")
        my_classes = 0
        while not my_classes:
            my_classes_num = input(
                "以下是您所授课程的所有班级信息：\n{}\n请选择>>>".format(classes_info)).strip()
            my_classes = classes_dict.get(my_classes_num, 0)
        try:
            self.teacher.bind_classes(my_classes)
        except Exception as e:
            logger.error(e)

    @auth(login)
    def teaching(self):
        """上课接口"""
        print("准备上课！")
        try:
            classes_info, classes_dict = self._query_classes(
                self.teacher.course)
            if not classes_info:
                raise ValueError("您所受课程{}还没有班级，请联系管理员！".format(
                    self.teacher.course.name))
            myclasses = 0
            while not myclasses:
                my_num = input("以下是您所受课程的所有班级信息：\n{}\n请选择>>>".format(
                    classes_info)).strip()
                myclasses = classes_dict.get(my_num, 0)
            print("尊敬的{}老师，感谢您为班级{}授课！".format(
                self.teacher.name, myclasses.name))
        except Exception as e:
            logger.error(e)

    @auth(login)
    def add_student_classes(self):
        """添加学生到班级"""
        print("开始添加学生入班级".center(30, "*"))
        print("第一步：选择学生".ljust(10, ">"))
        student_info, student_dict = self._query_student(self.teacher.course)
        if not student_info:
            raise ValueError("学生不存在！")
        current_student_list = []
        while True:
            current_student_num = input(
                "以下是选了您课程的学生信息：\n{}\n请选择>>>".format(student_info))
            current_student = student_dict.get(current_student_num, 0)
            if current_student:
                if current_student not in current_student_list:
                    current_student_list.append(current_student)
                else:
                    print("该学员您已经选中了！")
                    continue
            else:
                print("输入有误，请重试！")
                continue
            is_continue = input("1.继续添加  按其他任意键添加完毕").strip()
            if is_continue != "1":
                break
        print("学生选择完毕".rjust(10, "<"))

        print("第二步：选择班级".ljust(10, ">"))
        my_classes_list = self.teacher.classes
        my_classes_info_list = []
        for index, myclasses in enumerate(my_classes_list, 1):
            single_mycla_info = "{}.班级名称：{}  已收学员数量：{}  最大学员数量{}".format(
                index, myclasses.name,
                len(myclasses.students), myclasses.max_students
            )
            my_classes_info_list.append(single_mycla_info)
        myclasses_info = '\n'.join(my_classes_info_list)

        current_classes = 0
        while not current_classes:
            current_classes_num = input(
                "您管理的班级信息如下：\n{}\n请选择把学生加入到哪个班级>>>".format(myclasses_info)
            ).strip()
            try:
                current_classes = my_classes_list[int(current_classes_num) - 1]
            except IndexError as e:
                logger.debug(e)
                print("输入有误，请重试！")
            except ValueError as e:
                logger.debug(e)
                print("输入有误，请重试！")
        print("班级选择完毕".rjust(10, "<"))
        try:
            self.teacher.add_students(current_student_list, current_classes)
        except PermissionError as e:
            print(e)
            logger.debug(e)
        print("已完成本次操作".center(30, "*"))

    @auth(login)
    def modify_student_score(self):
        """"""
        info_list = []
        for classes in self.teacher.classes:
            for student in classes.students:
                single_student_info = '学生编号：{num}\t学生姓名：{sname}\t班级名称：{cname}'.format(
                    num=student.stu_no, sname=student.name, cname=classes.name)
                info_list.append(single_student_info)
        student_info = '\n'.join(info_list)
        if not student_info:
            print("您管理的班级还没有学员！")
            return

        current_student = 0
        while not current_student:
            choice_num = input("您管理的学生如下：\n{}\n请选择要修改的学生编号>>>".format(
                student_info)).strip()
            stu_info, stu_dict = self._query_student()
            current_student = stu_dict.get(choice_num, 0)

        issuccess = 0
        while not issuccess:
            try:
                new_score = input("学生{}当前成绩是{}\n请输入新成绩>>>".format(
                    current_student.name,
                    current_student.score))
                issuccess = self.teacher.modify_student_score(current_student,
                                                              int(new_score))
                print("您已成功将学生{}的成绩修改为{}".format(current_student.name,
                                                 new_score))
            except Exception as e:
                logger.error(e)


class AdminView(BaseView):
    """管理视图"""

    def __init__(self):
        super(AdminView, self).__init__()
        self.school = 0
        self.classes = 0
        self.route()

    def route(self):
        func_route = {
            "1": self.create_school,
            "2": self.create_course,
            "3": self.create_classes,
            "4": self.create_teacher,
            "5": exit
        }
        while True:
            act_num = input(
                "1.创建学校 2.创建课程 3.创建班级 4.创建讲师 5.退出程序，其他任意键退出管理视图\n>>>").strip()
            act_func = func_route.get(act_num, 0)
            if not act_func:
                self.school = 0
                break
            act_func()

    def login(self):
        if not self.school:
            logger.debug("admin begin login")
            while self.try_count < 3:
                print("请先登录！")
                school_name = input("请输入学校名称：\n>>>").strip()
                try:
                    self.school = super(AdminView, self).login(
                        '3', school_name)
                    logger.debug('login success')
                    print("登录成功！")
                    return True
                except ValueError as e:
                    print("没有这个学校")
                    logger.error(e)
            else:
                print("登录失败，已退出管理系统，请联系管理员")
                return False
        else:
            return True

    def create_school(self):
        """创建学校"""
        print("您正在创建学校".center(30, "*"))
        school_name = input("请输入学校名称：\n>>>")
        school_location = input("请输入学校位置：\n>>>")
        school_obj = sm.School(school_name, school_location)
        school_dict = upickle_from_file(self.school_path)
        school_dict[str(school_obj.num)] = school_obj
        pickle_to_file(self.school_path, school_dict)
        logger.debug('school {} created'.format(school_obj.name))
        print("学校{}已创建成功！".center(30, "*").format(school_obj.name))
        return school_obj

    @auth(login)
    def create_teacher(self):
        """创建讲师"""
        print("您正在创建讲师".center(30, "*"))
        school_info, school_dict = self._query_school()
        school_obj = 0
        while not school_obj:
            school_num = input(
                "学校信息如下：\n{}\n请选择为哪所学校创建讲师>>>".format(school_info)).strip()
            school_obj = school_dict.get(school_num, 0)
        teacher_name = input("请输入讲师姓名：\n>>>").capitalize().strip()
        teacher_age = input("请输入讲师年龄：").strip()
        teacher_sex = input("请输入讲师性别：").strip()
        course_info, course_dict = self._query_course(school_obj)
        teacher_course = 0
        while not teacher_course:
            teacher_course_num = input("请从以下课程列表里选择讲师的课程：\n{}\n>>>".format(
                course_info))
            teacher_course = course_dict.get(teacher_course_num, 0)
        teacher_salary = input("请输入讲师工资：\n>>>")
        teacher_obj = school_obj.create_teacher(teacher_name, teacher_age,
                                                teacher_sex, teacher_course,
                                                teacher_salary)
        print("讲师{}已创建成功！".center(30, "*").format(teacher_obj.name))
        # teacher_dict = upickle_from_file(self.teacher_path)
        # teacher_dict[teacher_obj.num] = teacher_obj
        # pickle_to_file(self.teacher_path, teacher_dict)
        return teacher_obj

    @auth(login)
    def create_course(self):
        """创建课程"""
        print("您正在创建课程".center(30, "*"))
        logger.debug('start create course')
        school_info, school_dict = self._query_school()
        school_obj = 0
        while not school_obj:
            school_num = input(
                "学校信息如下：\n{}\n请选择为哪所学校创建课程>>>".format(school_info)).strip()
            school_obj = school_dict.get(school_num, 0)
        # _, course_dict = self._query_course(school_obj)
        course_obj = 0
        while not course_obj:
            try:
                course_name = input("请输入课程名称：").strip().capitalize()
                course_cycle = input("请输入课程周期：")
                course_price = input("请输入课程价格：")
                course_obj = school_obj.create_course(
                    course_name, course_cycle, course_price)
                logger.debug('course {} created finish'.format(
                    course_obj.name))
                print("课程{}已创建成功！".center(30, "*").format(course_obj.name))
            except ValueError as e:
                logger.error(e)

    @auth(login)
    def create_classes(self):
        """创建班级接口"""
        print("您正在创建班级".center(30, "*"))
        logger.debug('starting create classes')

        school_info, school_dict = self._query_school()

        myschool = 0
        while not myschool:
            school_num = input(
                "以下是学校信息：\n{}\n请选择为哪所学校创建班级>>>".format(school_info))
            myschool = school_dict.get(school_num, 0)
            # classes_dict = upickle_from_file(self.classes_path)

        course_info, course_dict = self._query_course(myschool)
        mycourse = 0
        while not mycourse:
            course_num = input("该校区已开课程如下：\n{}\n请选择>>>".format(course_info))
            mycourse = course_dict.get(course_num, 0)
            if not mycourse:
                print("您输入的不正确，请重新选择")
        try:
            teacher_info, teacher_dict = self._query_teacher(mycourse)
            if not teacher_info:
                raise ValueError("{}课程还没有讲师，请联系管理员聘请！".format(mycourse.name))
        except ValueError as e:
            logger.error(e)
            return e
        myteacher = 0
        while not myteacher:
            teacher_num = input("以下是课程{}的讲师信息：\n{}\n请选择>>>".format(mycourse.name,
                                                                   teacher_info))
            myteacher = teacher_dict.get(teacher_num, 0)
            if not myteacher:
                print("输入错误，请重新选择！")
        try:
            classes_obj = myschool.create_classes(mycourse, myteacher)
            logger.debug('create classes[{}] end'.format(classes_obj.name))
            print("班级{}已创建成功！".center(30, "*").format(classes_obj.name))
            # classes_dict = upickle_from_file(self.classes_path)
            # classes_dict[classes_obj.num] = classes_obj
            return classes_obj
        except Exception as e:
            logger.error(e)


def view_factry(input_num):
    factry_dict = {"1": AdminView, "2": TeacherView, "3": StudentView}
    return factry_dict.get(input_num, 0)


def main():
    while True:
        view = 0
        while not view:
            input_num = input("1.管理视图  2.讲师视图  3.学员视图\n请选择>>>").strip()
            view = view_factry(input_num)
        view()
