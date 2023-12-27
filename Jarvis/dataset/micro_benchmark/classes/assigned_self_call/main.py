class MyClass:
    def __init__(self) -> None:
        pass

    def func1(self):
        pass

    def func2(self):
        a = self
        a.func1()


a = MyClass()
a.func2()

# class MyClass:
#     def func1(self):
#         self.func2()
#         pass
#
#     def func2(self):
#         a = self
#         a.func1()
#
# a = MyClass()
# a.func2()
