#! /usr/bin/env python
# -*- coding: utf-8 -*-
import bin.main
import util
import settings


def main():
    bin.main.main()
    # school_dict = util.upickle_from_file(
    #     settings.DATABASE["engineer"]["file"]["school"])
    # for num, school in school_dict.items():
    #     print(num, school.name)


if __name__ == '__main__':
    main()
