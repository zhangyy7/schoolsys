# # from enum import Enum

# # # Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May',
# # #                        'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

# # # for name, member in Month.__members__.items():
# # #     print(name, '=>', member, ',', member.value)

# # Counse = Enum('Counse', ('Python', 'Linux', 'Go'))

# # # for i in Counse:
# # #     print(i)

# # for name in Counse.__members__:
# #     print(name)

# from enum import Enum, unique


# @unique
# class Weekday(Enum):
#     Sun = 0
#     Mon = 1
#     Tue = 2
#     Wed = 3
#     Thu = 4
#     Fri = 5
#     Sat = 6

# day1 = Weekday.Mon

# print('day1 =', day1)
# print('Weekday.Tue =', Weekday.Tue)
# print('Weekday[\'Tue\'] =', Weekday['Tue'])
# print('Weekday.Tue.value =', Weekday.Tue.value)
# print('day1 == Weekday.Mon ?', day1 == Weekday.Mon)
# print('day1 == Weekday.Tue ?', day1 == Weekday.Tue)
# print('day1 == Weekday(1) ?', day1 == Weekday(1))

import traceback


def fun():
    s = traceback.extract_stack()
    caller = s[-2][2]
    print(type(caller))


def a(): fun()

a()
