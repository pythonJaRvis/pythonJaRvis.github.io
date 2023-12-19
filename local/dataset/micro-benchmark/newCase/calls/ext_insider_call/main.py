from from_module import ext_change

def func1():
    pass
def func2():
    pass
class cls:
    def __init__(self,fn) -> None:
        self.fn = fn
c = cls(func1)
ext_change(c,func2)
print(c.fn)
c.fn()