class base:
    def __init__(self):
        pass
    def __enter__(self):
        return self
    def __exit__(self,exc_type, exc_val, exc_tb):
        pass
class child(base):
    def __init__(self):
        pass
    def __enter__(self):
        return self
    def operate(self):
        pass

with child() as f:
    f.operate()
