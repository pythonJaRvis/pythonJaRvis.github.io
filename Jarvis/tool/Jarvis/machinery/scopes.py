#
# Copyright (c) 2020 Vitalis Salis.
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import symtable


import utils
import copy

class ScopeManager(object):
    """Manages the scope entries"""

    def __init__(self):
        self.scopes = {}
        self.copySeq = {}
    def handle_module(self, modulename, filename, contents):
        functions = []
        classes = []
        def process(namespace, parent, table):
            name = table.get_name() if table.get_name() != 'top' else ''
            if name:
                fullns = utils.join_ns(namespace, name)
            else:
                fullns = namespace

            if table.get_type() == "function":
                functions.append(fullns)

            if table.get_type() == "class":
                classes.append(fullns)

            sc = self.create_scope(fullns, parent)

            for t in table.get_children():
                process(fullns, sc, t)

        process(modulename, None, symtable.symtable(contents, filename, compile_type="exec"))
        return {"functions": functions, "classes": classes}

    def add_defi(self, ns, target, defi):
        scope = self.get_scope(ns)
        if scope:
            scope.add_def(target, defi)

    def handle_assign(self, ns, target, defi):
        scope = self.get_scope(ns)
        if scope:
            scope.add_def(target, defi)
    def add_params(self, ns, defi):
        scope = self.get_scope(ns)
        if scope:
            scope.add_params(defi)
    def get_def(self, current_ns, var_name):
        current_scope = self.get_scope(current_ns)
        while current_scope:
            defi= current_scope.get_def(var_name)
            if defi:
                return defi
            current_scope = current_scope.parent
    def get_scope(self, namespace):
        if namespace in self.get_scopes():
            return self.get_scopes()[namespace]

    def create_scope(self, namespace, parent):
        if not namespace in self.scopes:
            sc = ScopeItem(namespace, parent)
            self.scopes[namespace] = sc
        return self.scopes[namespace]

    def create_scope_by_name(self,dict_name,namespace,parent):
        if not namespace in self.scopes:
            sc = ScopeItem(namespace, parent)
            self.scopes[dict_name] = sc
        return self.scopes[dict_name]
    def add_scope(self,namespace,item,parent):
        if not namespace in self.scopes:
            self.scopes[namespace] = item
            item.parent = parent
    def get_scopes(self):
        return self.scopes

    def add_seq(self,ns):
        if ns in self.copySeq:
            self.copySeq[ns] += 1
        else:
            self.copySeq[ns] = 1
        return self.copySeq[ns]

    def get_seq(self,ns):
        if ns in self.copySeq:
            return self.copySeq[ns]
        return 0

    def add_inputs(self,ns,*args):
        scope = self.get_scope(ns)
        if scope:
            scope.add_inputs(args)

class ScopeItem(object):
    def __init__(self, fullns, parent):
        if parent and not isinstance(parent, ScopeItem):
            raise ScopeError("Parent must be a ScopeItem instance")

        if not isinstance(fullns, str):
            raise ScopeError("Namespace should be a string")

        self.parent = parent
        self.defs = {}
        self.lambda_counter = 0
        self.dict_counter = 0
        self.list_counter = 0
        self.if_counter = 0
        self.while_counter = 0
        self.fullns = fullns
        self.params = []
        self.inputs = set()
    def get_ns(self):
        return self.fullns

    def get_defs(self):
        return self.defs

    def add_params(self,defi):
        self.params.append(defi)
    def get_def(self, name):
        defs = self.get_defs()
        if name in defs:
            return defs[name]
        return None

    def add_inputs(self,*args):
        for i in args:
            self.inputs = self.inputs.union(i)
    def get_lambda_counter(self):
        return self.lambda_counter

    def get_dict_counter(self):
        return self.dict_counter

    def get_list_counter(self):
        return self.list_counter

    def get_if_counter(self):
        return self.if_counter

    def get_while_counter(self):
        return self.while_counter

    def inc_lambda_counter(self, val=1):
        self.lambda_counter += val
        return self.lambda_counter

    def inc_dict_counter(self, val=1):
        self.dict_counter += val
        return self.dict_counter

    def inc_list_counter(self, val=1):
        self.list_counter += val
        return self.list_counter

    def inc_if_counter(self,val=1):
        self.if_counter += val
        return self.if_counter

    def inc_while_counter(self,val=1):
        self.while_counter += val
        return self.while_counter

    def reset_counters(self):
        self.lambda_counter = 0
        self.dict_counter = 0
        self.list_counter = 0
        self.if_counter = 0
        self.while_counter = 0

    # 在scopt_item添加一个defi
    def add_def(self, name, defi):
        self.defs[name] = defi

    def merge_def(self, name, to_merge):
        if not name in self.defs:
            self.defs[name] = to_merge
            return

        self.defs[name].merge_points_to(to_merge.get_points_to())


    def get_prefix_defi(self,prefix:str)->list:
        defiNameList = []
        for defi in self.defs.values():
            if defi.get_ns().startswith(prefix):
                defiNameList.append(defi)
        return defiNameList

    def get_params_defiNs(self)->list:
        paramsDefiList = []
        for param in self.params:
            if param.get_type() == utils.constants.NAME_DEF:
                continue
            paramsDefiList += self.get_prefix_defi(param.get_ns())
        return paramsDefiList

    def __str__(self):
        def find_ns(ns):
            for defiNs,defi in self.defs.items():
                if defi.get_ns() == ns:
                    return defi
            return None
        ans = self.fullns
        ans += "-"
        for param in self.params:
            paramDefi = find_ns(param.get_ns())
            if not param:
                continue
            else:
                pointValue = param.get_last_point_value()
                if not pointValue:
                    tmp = param.get_ns() + ":" + "None"
                else:
                    tmp = param.get_ns() + ":" + utils.join_ns(*list(pointValue))
            ans += tmp
            ans += "-"
        return ans
class ScopeError(Exception):
    pass
