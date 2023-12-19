
class cls:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def foo(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


with cls() as f:
    f.foo()
