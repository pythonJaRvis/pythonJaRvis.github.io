class MyClass:
    def __init__(self) -> None:
        pass

    def func(self):
        def nested():
            pass

        nested()


a = MyClass()
a.func()
