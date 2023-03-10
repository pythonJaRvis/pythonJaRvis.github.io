
class ModuleManager:
    def __init__(self):
        self.internal = {}
        self.external = {}
        self.local = set()
    def create(self, name, fname, external=False):
        mod = Module(name, fname)
        if external:
            self.external[name] = mod
        else:
            self.internal[name] = mod
        return mod

    def get(self, name):
        if name in self.internal:
            return self.internal[name]
        if name in self.external:
            return self.external[name]

    def get_func_name(self,moduleNs,funcName):
        funcDict:Module = self.get(moduleNs)
        if funcName in funcDict.methods:
            return funcDict.methods[funcName]
    def get_internal_modules(self):
        return self.internal

    def get_external_modules(self):
        return self.external

    def add_local_modules(self,moduleNs):
        self.local.add(moduleNs)

    def get_local_modules(self):
        return self.local
class Module:
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename
        self.methods = dict()

    def get_name(self):
        return self.name

    def get_filename(self):
        return self.filename

    def get_methods(self):
        return self.methods

    def add_method(self, method, first=None, last=None):
        if not self.methods.get(method, None):
            self.methods[method] = dict(
                    name=method,
                    first=first,
                    last=last)
