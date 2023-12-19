def func1():
    pass


def func2():
    pass


class cls:
    def __init__(self, fn) -> None:
        self.fn = fn

    def change(self, fn):
        self.fn = fn


c = cls(func1)
c.change(func2)
c.fn()
