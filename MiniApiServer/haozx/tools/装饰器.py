# -*- coding: utf-8 -*-
# @Author: WildMan
# @Date: 2018/4/14

# def deco(arg):
#     def _deco(func):
#         def __deco():
#             print("before %s called [%s]." % (func.__name__, arg))
#             func()
#             print("  after %s called [%s]." % (func.__name__, arg))
#         return __deco
#     return _deco
#
# @deco("mymodule")
# def myfunc():
#     print(" myfunc() called.")
#
# @deco("module2")
# def myfunc2():
#     print(" myfunc2() called.")
#
# myfunc()
# myfunc2()

from functools import wraps
def wfoo(fuc):
    @wraps(fuc)
    def inner(*args,**kwargs):
        print('被修饰函数执行前')
        fuc(*args,**kwargs)
        print('被修饰函数执行后')
    return inner


def tokenCheck(func):
    @wraps(func)
    def check(*args,**kwargs):
        func(*args,**kwargs)
    return check




@wfoo
def foo():
    print('foo')
    return 'foo'
