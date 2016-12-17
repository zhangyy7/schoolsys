#! /usr/bin/env python
# -*-coding: utf-8 -*-
import util
from settings import COURSES, DATABASE, SCORE_RANGE

from . import classes


class School(object):
    """学校类"""

    def __init__(self, schoolname, location):
        """
        param name: 学校名称
        param location: 学校所在城市
        """
        self.name = schoolname
        self.location = location

    def create_classes(self, course_obj, teacher_obj):
        """创建班级"""
        # print(course_obj)
        clas_obj = classes.Classes(self)
        # print(clas_obj)
        clas_obj.course = course_obj
        clas_obj.teacher = teacher_obj
        print(clas_obj.num)
        # print("create_classes:clas_obj.course:", clas_obj.course)
        cla_path = DATABASE["engineer"]["file"]["classes"]
        cla_dict = util.upickle_from_file(cla_path)
        print(type(cla_dict), cla_dict)
        cla_dict[clas_obj.num] = clas_obj
        util.pickle_to_file(cla_path, cla_dict)
        return clas_obj

    def create_course(self, course_name, cycle, price):
        """创建课程"""
        course_obj = Course(self, course_name)
        course_obj.cycle = cycle
        course_obj.price = price
        cou_path = DATABASE["engineer"]["file"]["course"]
        cou_dict = util.upickle_from_file(cou_path)
        cou_dict[course_obj.name] = course_obj
        util.pickle_to_file(cou_path, cou_dict)
        return course_obj

    def create_teacher(self, name, age, sex, course, salary):
        """创建讲师"""
        teacher = Teacher(name, age, sex, self)
        teacher.course = course
        teacher.salary = salary

        teacher_path = DATABASE["engineer"]["file"]["teacher"]
        teacher_dict = util.upickle_from_file(teacher_path)
        teacher_dict[teacher.num] = teacher
        util.pickle_to_file(teacher_path, teacher_dict)
        return teacher


class Course(object):
    """课程类"""

    def __init__(self, creator, name):
        # print(isinstance(creator, School))
        self.name = name
        self.school = creator
        self.__cycle = 0
        self.__price = 0

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self)

    @property
    def cycle(self):
        return self.__cycle

    @cycle.setter
    def cycle(self, weeks):
        if weeks < COURSES[self.name]["cycle"]["min"]:
            print("这么短的时间爱因斯坦也学不会啊")
        elif weeks > COURSES[self.name]["cycle"]["max"]:
            print("学习周期太长了，招不到学生学校今年的开支你包了！")
        else:
            self.__cycle = weeks

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, amount):
        if amount < COURSES[self.name]["price"]["min"]:
            print("太便宜了，没利润喝西北风去啊！")
        elif amount > COURSES[self.name]["price"]["max"]:
            print("太贵了，招不到学生学校今年的开支你包了！")
        else:
            self.__price = amount


class SchoolMember(object):
    """学校成员基类，定义学校成员通用的基本属性"""

    member = 0

    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

    def enroll(self):
        SchoolMember.member += 1


class Teacher(SchoolMember):
    """讲师类，学校成员的一个子类"""

    teacher_num = 0

    def __init__(self, name, age, sex, creator):
        super(Teacher, self).__init__(name, age, sex)
        self.school = creator
        self.classes = 0
        self.__salary = 0
        self.num = Teacher.teacher_num + 1
        Teacher.teacher_num += 1

    def enroll(self, course, amount):
        super(Teacher, self).enroll()
        # 构造对象时默认为0，后续通过setter方法进行赋值
        if isinstance(course, Course):
            self.course = course
        else:
            print("只能传入课程")
            return "错误码"
        self.salary = amount

    def __set_salary(self, amount):
        """判断薪水范围"""

        amount = int(amount)
        if amount > COURSES[self.course.name]["salary"]["max"]:
            print("%s 讲师的薪水上限为%d,你咋不上天呢！" %
                  (self.course.name,
                   COURSES[self.course.name]["salary"]["max"]))
        elif amount < COURSES[self.course.name]["salary"]["min"]:
            print("%s 讲师的薪水最少也得%d,你打发要饭的呢！" %
                  (self.course.name,
                   COURSES[self.course.name]["salary"]["min"]))
        else:
            self.__salary = amount

    @property
    def salary(self):  # 私有属性__salery
        return self.__salary

    @salary.setter
    def salary(self, amount):
        """
        给私有变量__salery赋值，在这可以对amount的值做各种限制和判断
        在调用的时候形式上却和普通赋值并无二致，好评！
        """
        self.__set_salary(amount)

    def bind_classes(self, classes_obj):
        """绑定班级"""
        if isinstance(classes_obj, classes.Classes):
            if self.course == classes_obj.course and not classes_obj.teacher:
                self.classes = classes_obj
            else:
                raise KeyError('该班级已经有老师了')
        else:
            raise TypeError('只能绑定班级实例')

    def add_students(self, students):
        """把学生加入自己的班级，学生报名的语言必须与自己的班级一致"""
        # print(self.classes)
        for student in students:
            if student.course == self.course:
                self.classes.add_student(student, self)
                student.classes = self.classes

    def remove_students(self, students):
        """移除自己班级里的学员"""
        for student in students:
            if student.classes == self.classes:
                self.classes.remove_student(student, self)
                del student.classes


class Student(SchoolMember):
    """
    学生类，继承自学校成员类
    应该有学号 属性，作为学生的唯一标识，应该实例化时自动分配
    写成类属性程序重新运行还是会重置，暂时没有想到怎么实现
    """

    __stu_no = 0

    def __init__(self, name, age, sex):
        super(Student, self).__init__(name, age, sex)
        self.__school = 0
        self.__course = 0
        self.__ispaied = 0
        self.__tuition = 0
        self.__classes = 0
        self.__score = 0
        Student.stu_no += 1
        self.__num = Student.stu_no

    @property
    def stu_no(self):
        return self.__num

    @property
    def school(self):
        return self.__school

    @school.setter
    def school(self, school_obj):
        assert isinstance(school_obj, School)
        self.__school = school_obj

    @property
    def course(self):
        return self.__course

    @course.setter
    def course(self, course_obj):
        assert isinstance(course_obj, Course)
        self.__course = course_obj

    @property
    def ispaied(self):
        return self.__ispaied

    @ispaied.setter
    def ispaied(self, value):
        assert value in [0, 1]
        self.__ispaied = int(value)

    @property
    def tuition(self):
        return self.__tuition

    @tuition.setter
    def tuition(self, amount):
        assert amount == self.course.price
        self.__tuition = amount

    def enroll(self, school, course):
        """注册方法"""
        super(Student, self).enroll()
        assert isinstance(school, School), isinstance(course, Course)
        self.school = school
        self.course = course

    def pay_tuition(self, amount):
        """交学费方法"""
        if int(amount) >= self.course.price:
            self.tuition = self.course.price
            self.ispaied = 1
            return True

    @property
    def classes(self):
        return self.__classes

    @classes.setter
    def classes(self, classes_obj):
        assert isinstance(
            classes_obj, classes.Classes),\
            'the value must be a instance of classes'
        if self.ispaied:
            self.__classes = classes_obj
        else:
            raise ValueError('no paied the course')

    @classes.deleter
    def classes(self):
        self.__classes = 0

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        """设置分数"""
        if SCORE_RANGE["min"] <= int(value) <= SCORE_RANGE["max"]:
            self.__score = value
        else:
            raise ValueError('score must between {min}-{max}'.format(
                min=SCORE_RANGE["min"], max=SCORE_RANGE["max"]))
