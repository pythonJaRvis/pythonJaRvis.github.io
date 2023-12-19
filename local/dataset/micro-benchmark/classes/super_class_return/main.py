class A:
    def __init__(self) -> None:
        pass

    def func1(self):
        pass


class B(A):
    def __init__(self) -> None:
        super().__init__()

    def func2(self):
        return self.func1


b = B()
fn = b.func2()
fn()
