def func1():
    pass


def func2():
    pass


class cls:
    def __init__(self, fn) -> None:
        self.fn = fn


c = cls(func1)


def change():
    c.fn = func2


change()
c.fn()
