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
import re
import utils

IF_FLAG = "<if"
WHILE_FLAG = "<while"
ELSE_FLAG = "<els"
COPY_FLAG = "<copy"
LIST_FLAG = "<list"
DICT_FLAG = "<dict"


class CallGraph(object):
    def __init__(self):
        self.cg = {}
        self.modnames = {}

    def add_node(self, name, modname=""):
        if not isinstance(name, str):
            raise CallGraphError("Only string node names allowed")
        if not name:
            return
            raise CallGraphError("Empty node name")

        if not name in self.cg:
            self.cg[name] = set()
            self.modnames[name] = modname

        if name in self.cg and not self.modnames[name]:
            self.modnames[name] = modname

    def add_edge(self, src, dest):
        if not src:
            return
        def process_str(s: str):
            if IF_FLAG in s or ELSE_FLAG in s or WHILE_FLAG in s or LIST_FLAG in s or DICT_FLAG in s:
                s_list = s.split(".")
                s_list = list(map(lambda x: None if IF_FLAG in x or ELSE_FLAG in x or WHILE_FLAG in x or LIST_FLAG in x
                or DICT_FLAG in x else x, s_list))
                s_list = list(filter(lambda x:x,s_list))
                return ".".join(s_list)
            else:
                return s
        if utils.constants.RETURN_NAME in src or utils.constants.RETURN_NAME in dest:
            return
        src = process_str(src)
        dest = process_str(dest)
        if dest == '<str>':
            return
        if dest == '<int>':
            return
        # print(src,"调用了",dest)
        self.add_node(src)
        self.add_node(dest)
        self.cg[src].add(dest)

    def add_edges(self,src,destList):
        self.add_node(src)
        for dest in destList:
            self.add_node(dest)
            self.cg[src].add(dest)
    def is_exist_edge(self, src, dst):
        if not src in self.cg:
            return False
        return dst in self.cg[src]

    def get(self):
        return self.cg

    def existEdge(self,src):
        if src in self.cg and self.cg[src]:
            return True
        return False

    def get_edges(self):
        output = []
        for src in self.cg:
            for dst in self.cg[src]:
                output.append([src, dst])
        return output

    def get_modules(self):
        return self.modnames


class CallGraphError(Exception):
    pass
