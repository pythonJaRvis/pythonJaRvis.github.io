class Resource():
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def operate(self):
        pass
with Resource() as res:
    res.operate()