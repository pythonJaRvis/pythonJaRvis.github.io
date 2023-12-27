class B:
    def funcb(self):
        self.smth = self.func

    def func(self):
        pass


class A(B):
    def __init__(self) -> None:
        pass

    def funca(self):
        self.smth = self.func

    def func(self):
        pass


a = A()
a.funcb()
a.smth()

a.funca()
a.smth()
