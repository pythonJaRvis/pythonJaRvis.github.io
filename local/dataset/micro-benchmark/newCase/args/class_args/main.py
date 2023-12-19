def func1():
    pass


def func2():
    pass


class cls:
    def __init__(self, fn) -> None:
        self.fn = fn


cls1 = cls(func1)
cls2 = cls(func2)
cls2.fn()
