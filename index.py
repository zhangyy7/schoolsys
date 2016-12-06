#!  /usr/bin/env python
# -*- coding: utf-8 -*-

from core.course import Course
from core.schoolmember import Teacher


def main():
    python = Course('Python')
    python.cycle = 36
    python.price = 15000

    t1 = Teacher('Alex', 28, 'M', python)
    t1.salary = 70000
    print(t1)

main()
