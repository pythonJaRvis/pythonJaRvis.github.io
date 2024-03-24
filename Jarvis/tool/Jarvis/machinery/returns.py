import utils


class ReturnManager(object):
    def __init__(self):
        self.returns = {}

    def get_return(self):
        return self.returns

    def add_returnitem(self,currentNs ,left  , row , right:str):
        right = utils.join_ns(*right.split(".")[:-1])
        item = ReturnItem(left,row,right)
        if  not currentNs in self.returns:
            self.returns[currentNs] = []
        self.returns[currentNs].append(item)


    def get_returnitem(self,currentNs):
        if currentNs in self.returns:
            return self.returns[currentNs]
    def pop_returnItem(self,currentNs,row,funcName):
        if not currentNs in self.returns:
            return None
        for item in self.returns[currentNs]:
            if item.row == row and item.right == funcName:
                self.returns[currentNs].remove(item)
                return item.left

    def peek_returnItem(self,currentNs,row,funcName):
        if not currentNs in self.returns:
            return None
        for item in self.returns[currentNs]:
            if item.row == row and item.right == funcName:
                return item.left


class ReturnItem:
    def __init__(self,left , row , right):
        self.left = left
        self.row = row
        self.right = right

