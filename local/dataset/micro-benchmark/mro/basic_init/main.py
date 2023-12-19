class A:
    def __init__(self):
        pass


class B(A):
    def __init__(self):
        super().__init__()

    def func(self):
        pass


b = B()
b.func()
