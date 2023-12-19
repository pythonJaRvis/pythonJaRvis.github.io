def func1():
    pass


def func2():
    pass


class cls:
    def __init__(self, func=func1) -> None:
        self.fn = func


c = cls(func2)
c.fn()
