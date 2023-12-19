def func1():
    pass


def func2():
    pass


var1 = func1
var2 = var1
var1 = func2
var2()
