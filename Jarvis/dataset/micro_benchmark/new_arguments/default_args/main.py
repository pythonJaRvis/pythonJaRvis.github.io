def func1():
    pass


def func2():
    pass


def func(args1, args2=func1):
    args1()
    args2()


func(func2, func2)
