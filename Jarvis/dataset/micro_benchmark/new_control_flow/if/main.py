def func1():
    pass


def func2():
    pass


def func3():
    pass


class Cls_a:
    def __init__(self) -> None:
        self.fn = func1


class Cls_b:
    def __init__(self) -> None:
        self.fn = func2


class Cls_c:
    def __init__(self) -> None:
        self.fn = func3


c = Cls_a()
if id(c) % 2 == 0:
    c = Cls_b()
else:
    c = Cls_c()
c.fn()
