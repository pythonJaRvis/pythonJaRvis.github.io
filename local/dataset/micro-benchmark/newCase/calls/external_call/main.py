from from_module import change


def local_func():
    pass


class cls:
    def __init__(self, fn) -> None:
        self.fn = fn


c = cls(local_func)
change(c)
c.fn()
