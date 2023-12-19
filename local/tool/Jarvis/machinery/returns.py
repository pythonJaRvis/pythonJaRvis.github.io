# Copyright [pythonJaRvis] [name of copyright owner]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import utils


class ReturnManager(object):
    def __init__(self):
        self.returns = {}

    def get_return(self):
        return self.returns

    def add_returnitem(self, currentNs, left, row, right: str):
        right = utils.join_ns(*right.split(".")[:-1])
        item = ReturnItem(left, row, right)
        if not currentNs in self.returns:
            self.returns[currentNs] = []
        self.returns[currentNs].append(item)

    def get_returnitem(self, currentNs):
        if currentNs in self.returns:
            return self.returns[currentNs]

    def pop_returnItem(self, currentNs, row, funcName):
        if not currentNs in self.returns:
            return None
        for item in self.returns[currentNs]:
            if item.row == row and item.right == funcName:
                self.returns[currentNs].remove(item)
                return item.left

    def peek_returnItem(self, currentNs, row, funcName):
        if not currentNs in self.returns:
            return None
        for item in self.returns[currentNs]:
            if item.row == row and item.right == funcName:
                return item.left


class ReturnItem:
    def __init__(self, left, row, right):
        self.left = left
        self.row = row
        self.right = right
