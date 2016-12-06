#!  /usr/bin/env python
# -*- coding: utf-8 -*-
import setting
from core.school import School


print(setting.BASE_PATH)


def main():
    shanghai = School("oldboyedu", "shanghai")
    shanghai.create_course('Python')

main()
