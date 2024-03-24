

class NodeManager:
    def __init__(self):
        self.nodes = {}
    def add(self,ns,node):
        if ns in self.nodes:
            return
        self.nodes[ns] = node
    def get(self,ns):
        if ns in self.nodes:
            return self.nodes[ns]
        return None