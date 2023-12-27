class A:
    def __init__(self):
        pass

    def func(self):
        pass


class B(A):
    def __init__(self):
        pass

    pass


class C(A):
    def __init__(self):
        pass

    def func(self):
        pass


class D(B, C):
    def __init__(self):
        pass

    pass


d = D()
d.func()
