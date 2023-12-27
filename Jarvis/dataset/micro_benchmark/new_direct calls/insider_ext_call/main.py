from from_module import ext_change


def func1():
    pass


def func2():
    pass


class cls:
    def __init__(self, fn) -> None:
        self.fn = fn


c = cls(func1)


def local_change():
    ext_change(c, func2)


local_change()
c.fn()
