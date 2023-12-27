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
import heapq

class CallManager(object):
    def __init__(self):
        self.calls = {}
        self.seq = 1


    def call(self,row,func_name,ns,params,inherit = False):
        dict_all = {}
        paramList = []
        for param in params:
            if isinstance(param ,dict):
                dict_all.update(param)
            else:
                paramList.append(param)
        if dict_all:
            paramList.append(dict_all)
        item = CallItem(row,self.seq,func_name,ns,paramList,inherit)
        if not self.calls.__contains__(ns):
            self.calls[ns] = []
        heapq.heappush(self.calls[ns],item)
        self.seq += 1

    def get(self,callNs):
        if callNs in self.calls:
            return self.calls[callNs]
class CallItem(object):
    types = [
        utils.constants.FUN_DEF,
        utils.constants.CLS_DEF,
        utils.constants.EXT_DEF,
        utils.constants.NA_DEF
    ]

    def __init__(self,row :int,seq:int,funcDefi:str ,ns:str , params:set,inherit):
        self.row = row
        self.funcDefi = funcDefi
        self.seq = seq
        self.ns = ns
        self.params = params
    def get_ns(self):
        return self.ns

    def __lt__(self, other):
        return self.row < other.row or self.seq < other.seq

