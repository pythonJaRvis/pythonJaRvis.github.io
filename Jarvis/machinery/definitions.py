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

import utils
import heapq
import math
from machinery import gol

class PointItem(object):
    def __init__(self, row, values=set()):
        if isinstance(values, list):
            values = set(values)
        elif isinstance(values,str):
            values = set([values])
        self.points_to = values
        self.row = row
    def __lt__(self, other):
        return self.row < other.row


class DefinitionManager(object):
    def __init__(self):
        self.defs = {}
        self.copyMap = {}
    # 创建一个def_type类型的ns defi
    def create(self, ns, def_type):
        if not ns or not isinstance(ns, str):
            raise DefinitionError("Invalid namespace argument")
        if def_type not in Definition.types:
            raise DefinitionError("Invalid def type argument")
        if self.get(ns):
            raise DefinitionError("Definition already exists")
        self.defs[ns] = Definition(ns, def_type)

        return self.defs[ns]

    def create_by_name(self,dict_name,ns, def_type):
        if not ns or not isinstance(ns, str):
            raise DefinitionError("Invalid namespace argument")
        if def_type not in Definition.types:
            raise DefinitionError("Invalid def type argument")
        if self.get(dict_name):
            raise DefinitionError("Definition already exists")
        self.defs[dict_name] = Definition(ns, def_type)

        return self.defs[dict_name]


    def get(self, ns) :
        if ns in self.defs:
            return self.defs[ns]
        return None

    def addCopy(self,copyNs,ns):
        copyDefi = self.defs.get(copyNs)
        copyDefi.isCopy = True
        self.copyMap[copyNs] = ns
    def getOrCreate(self, ns, def_type):
        if not self.get(ns):
            return self.create(ns, def_type)

    def get_defs(self):
        return self.defs

    def handle_function_def(self, parent_ns, fn_name):
        full_ns = utils.join_ns(parent_ns, fn_name)
        defi = self.get(full_ns)
        if not defi:
            defi = self.create(full_ns, utils.constants.FUN_DEF)
            defi.decorator_names = set()
        else:
            defi.decorator_names = set()
        defi.def_type = utils.constants.FUN_DEF
        return_ns = utils.join_ns(full_ns, utils.constants.RETURN_NAME)
        if not self.get(return_ns):
            self.create(return_ns, utils.constants.RETURN_DEF)

        return defi

    def handle_class_def(self, parent_ns, cls_name,cls_ns):
        full_ns = utils.join_ns(cls_ns, cls_name)
        defi: Definition = self.get(full_ns)
        if not defi:
            defi = self.create(full_ns, utils.constants.CLS_DEF)
        else:
            defi.def_type = utils.constants.CLS_DEF
        return defi

    def handle_if_def(self, parent_ns, if_name,def_type = utils.constants.IF_DEF):
        full_ns = utils.join_ns(parent_ns, if_name)
        defi = self.get(full_ns)
        if not defi:
            defi = self.create(full_ns,def_type)
        return defi

    def transform_defi(self, ns, row) -> list:
        defi: Definition = self.defs.get(ns)
        transDefiNames = []
        for point_ns in defi.get_name_pointer(row):
            transDefiNames.append(point_ns)
        return transDefiNames

    def get_final_pointName(self, defiNs, row):
        curDefi: Definition = self.get(defiNs)
        if not curDefi:
            return [defiNs], row
        if not curDefi.points:
            return [defiNs], row
        # pointItem: PointItem = curDefi.get_point(row)
        pointValues:set() = curDefi.get_last_point_value()
        if not pointValues:
            pointValues = curDefi.get_last_point_value()
            if not pointValues:
                return [defiNs],row
        return pointValues,row

    def get_scope_name(self, ns: str):
        while ns.rfind('.') != -1:
            rIndex = ns.rfind('.')
            scopeNs = ns[:rIndex]
            if self.get(scopeNs) and self.get(scopeNs).get_type() in [utils.constants.MOD_DEF,
                                                                      utils.constants.CLS_DEF,
                                                                      utils.constants.FUN_DEF,
                                                                      ]:
                return scopeNs
            ns = scopeNs

    def get_module_name(self, ns: str):
        while ns.rfind('.') != -1:
            rIndex = ns.rfind('.')
            moduleNs = ns[:rIndex]
            if self.get(moduleNs) and self.get(moduleNs).get_type() == utils.constants.MOD_DEF:
                return moduleNs
            ns = moduleNs

    def is_same_scope(self, first, second):
        return self.get_scope_name(first) == self.get_scope_name(second)

    def helper(self, defiNs, row):
        curDefi: Definition = self.get(defiNs)
        if not curDefi:
            return defiNs
        if not curDefi.points:
            return defiNs

    def get_last_final_pointName(self, defiNs) -> list:
        queue = [defiNs]
        finalDefiNsList = []
        while queue:
            curDefiNs = queue[0]
            queue.remove(curDefiNs)
            curDefi: Definition = self.get(curDefiNs)
            curItemLists = curDefi.get_last_point_value()
            if not curItemLists:
                finalDefiNsList.append(curDefiNs)
            else:
                queue += curItemLists
        return finalDefiNsList


class Definition(object):
    types = [
        utils.constants.FUN_DEF,
        utils.constants.MOD_DEF,
        utils.constants.NAME_DEF,
        utils.constants.CLS_DEF,
        utils.constants.EXT_DEF,
        utils.constants.IF_DEF,
        utils.constants.ELSE_DEF,
        utils.constants.WHILE_DEF,
        utils.constants.PARAM_DEF,
        utils.constants.NA_DEF,
        utils.constants.RETURN_DEF,
        utils.constants.INT_DEF,
        utils.constants.STR_DEF,
        utils.constants.LIST_DEF,
        utils.constants.MAP_DEF,
    ]

    def __init__(self, fullns, def_type):
        self.fullns = fullns
        self.def_type = def_type
        self.points = []
        self.bias = set()
        self.lines = set()

    def get_point(self, row) -> PointItem:
        cur_point = None
        for point in self.points:
            if point.row <= row:
                cur_point = point
            else:
                break
        return cur_point

    def clear_point(self):
        self.points = []

    # 添加一个namePointItem

    def add_value_point(self, row, values):
        curPoint = None
        point = PointItem(row, values)
        heapq.heappush(self.points, point)
        if isinstance(values,str):
            values = [values]
        if not gol.get_value('precision'):
            self.bias = self.bias.union(set(values))

    def get_type(self):
        return self.def_type

    def is_function_def(self):
        return self.def_type == utils.constants.FUN_DEF

    def is_ext_def(self, row=0):
        return self.def_type == utils.constants.EXT_DEF

    def is_callable(self):
        return self.is_function_def() or self.is_ext_def()

    # 拿到PointItem的value

    def get_name(self):
        return self.fullns.split(".")[-1]

    def get_ns(self):
        return self.fullns



    def get_last_point_value(self):
        if not self.points:
            return set()
        return self.points[len(self.points) - 1].points_to.union(self.bias)
    def set_element(self,key,value):
        if self.def_type not in [utils.constants.LIST_DEF, utils.constants.MAP_DEF]:
            return
            # raise DefinitionError("the definition doesn't belong to [List or Dict]")
        if not getattr(self,'memo',None):
            self.memo = {}
        self.memo[key] = value

    def get_element(self,key):
        if key not in self.memo:
            return []
        return self.memo[key]
    def del_element(self,key):
        if self.def_type not in [utils.constants.LIST_DEF, utils.constants.MAP_DEF]:
            raise DefinitionError("the definition doesn't belong to [List or Dict]")
        if not getattr(self,'memo'):
            return
        del self.memo[key]
class ChangeManager:
    def __init__(self):
        self.changes = {}

    def getChange(self, ns):
        if ns in self.changes:
            return self.changes[ns]
        self.changes[ns] = {}
        return self.changes[ns]

    def addChange(self, ns, defins, row, values):
        if ns not in self.changes:
            self.changes[ns] = {}
        item = ChangeItem(row, values)
        if defins not in self.changes[ns]:
            # self.changes[ns].setdefault(defins, item)
            self.changes[ns][defins] = item
        else:
            self.changes[ns].get(defins).addPoint(row,values)

class ChangeItem(Definition):
    def __init__(self, row, values,if_union = False):
        self.points = []
        self.bias = set()
        self.if_union = if_union
        self.add_value_point(row,values)
    def addPoint(self,row,values):
        point = PointItem(row,values)
        heapq.heappush(self.points,point)
class DefinitionError(Exception):
    pass
