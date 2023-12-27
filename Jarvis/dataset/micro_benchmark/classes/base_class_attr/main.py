class A:
    def __init__(self) -> None:
        pass

    class B:
        def __init__(self) -> None:
            pass

        def bfunc(self):
            pass


class C(A.B):
    def __init__(self) -> None:
        pass

    def cfunc(self):
        pass


c = C()
c.cfunc()
c.bfunc()
