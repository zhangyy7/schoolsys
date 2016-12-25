# 这是一个模拟学校选课系统的程序

### 作者介绍：
* author：zhangyy
* nickname:逆光穿行
* github:[zhangyy.com](https://github.com/zhangyy7)

### 功能介绍：
* 管理视图：创建学校、课程、讲师、班级
* 讲师视图：绑定班级、修改学生成绩、添加学生到班级
* 学生视图：注册、交学费、选班级

### 环境依赖：
* Python3.5.2

### 目录结构：

    schoolsys
    ├── index.py
    ├── README.md
    ├── settings.py #配置文件
    ├── util.py 通用工具函数
    ├── bin
    │   ├── __init__.py
    │   └── main.py #主函数
    ├── core #程序核心目录
    │   ├── __init__.py
    │   ├── classes.py #班级类
    │   ├── schoolmember.py #学校成员相关类：学校、学生、讲师等，包含程序底层逻辑
    │   └── view.py #视图相关类，包含用户交互逻辑
    ├── data #数据文件目录
    │   ├── schools.pickle
    │   ├── classes.pickle
    │   ├── course.pickle
    |   ├── students.pickle
    │   └── teachers.pickle
    └── logs #程序日志目录
        └── school.log #程序日志



###运行说明：
* 运行index.py文件，根据提示完成操作。
* 需要先进管理视图创建学校、课程、班级、讲师，每一步都有提示，根据提示操作就可以了。
* 老师的工资范围和课程的价格范围可在settings里配置。