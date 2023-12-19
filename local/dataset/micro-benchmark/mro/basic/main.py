class A:
    def __init__(self) -> None:
        pass

    def func(self):
        pass


class B(A):
    def __init__(self) -> None:
        super().__init__()

    pass


b = B()
b.func()
