# #
# # Copyright (c) 2020 Vitalis Salis.
# #
# # Licensed to the Apache Software Foundation (ASF) under one
# # or more contributor license agreements.  See the NOTICE file
# # distributed with this work for additional information
# # regarding copyright ownership.  The ASF licenses this file
# # to you under the Apache License, Version 2.0 (the
# # "License"); you may not use this file except in compliance
# # with the License.  You may obtain a copy of the License at
# #
# #   http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing,
# # software distributed under the License is distributed on an
# # "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# # KIND, either express or implied.  See the License for the
# # specific language governing permissions and limitations
# # under the License.
# #
import ast
import utils
from machinery.callgraph import CallGraph
from machinery.calls import CallItem
from machinery.scopes import ScopeItem, ScopeManager
from machinery.definitions import Definition, DefinitionManager
from machinery.modules import ModuleManager
from machinery.returns import ReturnManager
import copy
import math
from functools import reduce


#
# class NsRow:
#     def __init__(self, ns, row):
#         self.ns = ns
#         self.row = row
# class CallGraphProcessor():
#     def __init__(self,input_file, input_mod,
#             scope_manager, def_manager, class_manager,
#             module_manager,call_manager, call_graph,return_manager,modules_analyzed=None):
#         self.input_file = input_file
#         self.input_mod = input_mod
#         self.module_analyzed = modules_analyzed
#         self.scope_manager:ScopeManager = scope_manager
#         self.def_manager:DefinitionManager = def_manager
#         self.class_manager = class_manager
#         self.module_manager:ModuleManager = module_manager
#         self.call_graph:CallGraph = call_graph
#         self.call_manager:call_manager = call_manager
#         self.format = set()
#         self.return_manager:ReturnManager = return_manager
#         self.selfMap = {}
#         self.calledFuncSet:set = set()
#         self.calledScope = {}
#     def analyze(self):
#         self.get_call_graph()
#
#     def get_all_reachable_functions(self):
#         reachable = set()
#         names = set()
#         current_scope = self.scope_manager.get_scope(self.current_ns)
#         while current_scope:
#             for name, defi in current_scope.get_defs().items():
#                 if defi.is_function_def() and not name in names:
#                     closured = self.closured.get(defi.get_ns())
#                     for item in closured:
#                         reachable.add(item)
#                     names.add(name)
#             current_scope = current_scope.parent
#
#         return reachable
#
#     def has_ext_parent(self, node):
#         if not isinstance(node, ast.Attribute):
#             return False
#
#         while isinstance(node, ast.Attribute):
#             parents = self._retrieve_parent_names(node)
#             for parent in parents:
#                 for name in self.closured.get(parent, []):
#                     defi = self.def_manager.get(name)
#                     if defi and defi.is_ext_def():
#                         return True
#             node = node.value
#         return False
#
#     def get_full_attr_names(self, node):
#         name = ""
#         while isinstance(node, ast.Attribute):
#             if not name:
#                 name = node.attr
#             else:
#                 name = node.attr + "." + name
#             node = node.value
#
#         names = []
#         if getattr(node, "id", None) == None:
#             return names
#
#         defi = self.scope_manager.get_def(self.current_ns, node.id)
#         if defi and self.closured.get(defi.get_ns()):
#             for id in self.closured.get(defi.get_ns()):
#                 names.append(id + "." + name)
#         return names
#
#     def is_builtin(self, name):
#         return name in __builtins__
#
#     # 返回函数的scope，还需要加上参数
#     def dfs(self,callNs:str,item:CallItem = None) ->ScopeItem:
#         # 如果这个方法没有解析，直接返回
#         curScope = self.scope_manager.get_scope(callNs)
#         if not curScope:
#             return callNs
#         if str(curScope) in self.calledScope:
#             return self.calledScope[str(curScope)]
#         curDefi:Definition = self.def_manager.get(callNs)
#         if curDefi.get_type() not in [utils.constants.IF_DEF, utils.constants.ELSE_DEF]:
#             self.call_graph.add_node(callNs)
#         callItemList = self.call_manager.get(callNs)
#         # 将函数匹配起来
#         if not callItemList:
#             return self.scope_manager.get_scope(callNs)
#         for callItem in callItemList:
#             defi:Definition = self.def_manager.get(callItem.func_name)
#             if defi and defi.get_type() in [utils.constants.IF_DEF]:
#                 self.call_if(callNs,callItem)
#                 continue
#             if "|||" in callItem.func_name:
#                 self.call_else(callNs,callItem)
#                 continue
#             calleeNsList = self.resolve(callItem.func_name,callItem.row+1,True)
#             for calleeNs in calleeNsList:
#                 if calleeNs not in self.calledFuncSet:
#                     self.calledFuncSet.add(calleeNs)
#                     self.call(callNs,calleeNs,callItem)
#                     self.calledFuncSet.remove(calleeNs)
#         self.calledScope[str(curScope)] = copy.deepcopy(curScope)
#         return curScope
#
#     def call_if(self,callNs , callItem:CallItem):
#         print(callNs)
#         calleeNs = callItem.func_name
#         calleeScope: ScopeItem = self.scope_manager.get_scope(calleeNs)
#         calleeNs = calleeScope.get_ns()
#         copyScope = copy.deepcopy(calleeScope)
#         # 完成pfg的更新
#         calleeScope = self.dfs(calleeNs, callItem)
#         # self.match_return(callNs, callItem)
#         # self.update_only_if(callNs,calleeScope,callItem)
#         self.update_if(callNs,calleeScope,callItem)
#         self.reset_scope(calleeScope, copyScope)
#         pass
#
#     def update_if(self,callNs:str,calleeScope:ScopeItem,callItem:CallItem):
#
#         for defiNs,defi in calleeScope.get_defs().items():
#             curDefiNs = utils.join_ns(callNs,defiNs)
#             curDefi:Definition = self.def_manager.get(curDefiNs)
#             if not curDefi:
#                 curDefi = self.def_manager.create(curDefiNs, utils.constants.NAME_DEF)
#             pointNsList = self.resolve(utils.join_ns(calleeScope.get_ns(),defiNs),math.inf)
#             tmpPoint = curDefi.add_name_point(callItem.row)
#             for point in pointNsList:
#                 tmpPoint.add(point)
#         pass
#
#     def update_only_if(self,callNs:str,calleeScope:ScopeItem,callItem:CallItem):
#         for defiNs,defi in calleeScope.get_defs().items():
#             curDefiNs = utils.join_ns(callNs,defiNs)
#             curDefi:Definition = self.def_manager.get(curDefiNs)
#             if not curDefi:
#                 curDefi = self.def_manager.create(curDefiNs, utils.constants.NAME_DEF)
#             pointNsList = self.resolve(utils.join_ns(calleeScope.get_ns(),defiNs),math.inf)
#             tmpPoint = curDefi.get_point_value(callItem.row)
#             for point in pointNsList:
#                 tmpPoint.add(point)
#         pass
#
#     def call_else(self,callNs , callItem:CallItem):
#         calleeNsList = callItem.func_name.split("|||")
#         calleeIf,calleeElse = calleeNsList
#         callifScope: ScopeItem = self.scope_manager.get_scope(calleeIf)
#         callelseScope: ScopeItem = self.scope_manager.get_scope(calleeElse)
#         callifNs = callifScope.get_ns()
#         callelseNs = callelseScope.get_ns()
#         copyIfScope = copy.deepcopy(callifScope)
#         copyElseScope = copy.deepcopy(callelseScope)
#         # 完成pfg的更新
#         callifScope = self.dfs(callifNs, callItem)
#         callelseScope = self.dfs(callelseNs,callItem)
#         self.merge_if_else(callifScope,callelseScope)
#         self.update_if(callNs, callelseScope, callItem)
#         self.reset_scope(callifScope, copyIfScope)
#         self.reset_scope(callelseScope, copyElseScope)
#         pass
#     def merge_if_else(self,ifScope:ScopeItem,elseScope:ScopeItem):
#         elseScopeNs = elseScope.get_ns()
#         for defiNs,defi in ifScope.get_defs().items():
#             elseDefiNs = utils.join_ns(elseScopeNs,defiNs)
#             elseDefi:Definition = self.def_manager.get(elseDefiNs)
#             if not elseDefi:
#                 elseDefi = defi
#                 self.scope_manager.handle_assign(elseScope.get_ns(),elseDefiNs.replace(elseScope.get_ns(),'')[1:],elseDefi)
#             else:
#                 pointNsList = self.resolve(utils.join_ns(ifScope.get_ns(),defiNs),math.inf)
#                 tmpElsePoint = elseDefi.get_last_point()
#                 if not tmpElsePoint:
#                     return
#                 for point in pointNsList:
#                     tmpElsePoint.points_to.add(point)
#         pass
#     def get_call_graph(self):
#         for callNs in self.def_manager.entrySet:
#             if callNs not in self.call_graph.cg:
#                 self.dfs(callNs)
#             # if callNs not in self.call_graph.cg and self.def_manager.get(callNs).get_type() == utils.constants.MOD_DEF:
#             #     self.dfs(callNs)
#         # self.dfs('request')
#
#     # 将calleeNS转变成真正的指向
#     def resolve(self,calleeNs:str,row:int ,flag = False)->list:
#         calleeDefi:Definition = self.def_manager.get(calleeNs)
#         # if not calleeDefi:
#         #     return [calleeNs]
#         if not calleeDefi or  calleeDefi.get_type() in [utils.constants.NAME_DEF, utils.constants.NA_DEF,
#                                                        utils.constants.PARAM_DEF, utils.constants.RETURN_DEF]:
#             # nsRowList = self.get_point([''], self.convectStrtoList(calleeNs), row)
#             nsRowList = self.get_point(calleeNs, row)
#             for nsRow in nsRowList:
#                 if nsRow.ns == calleeNs:
#                     return list(map(lambda x:x.ns,nsRowList))
#                 if calleeNs in nsRow.ns:
#                     return list(map(lambda x: x.ns, nsRowList))
#             returnDefiNsList = []
#             for nsRow in nsRowList:
#                 defiList = self.resolve(nsRow.ns, nsRow.row,flag)
#                 returnDefiNsList += defiList
#             return returnDefiNsList
#         if not calleeDefi:
#             return [calleeNs]
#         if calleeDefi.get_type() in [utils.constants.FUN_DEF, utils.constants.EXT_DEF]:
#             return [calleeNs]
#         if calleeDefi.get_type() == utils.constants.CLS_DEF:
#             return [utils.join_ns(calleeNs, utils.constants.CLS_INIT)] if flag else [calleeNs]
#         elif calleeDefi.get_type() == utils.constants.INT_DEF:
#             return ['<int>']
#         elif calleeDefi.get_type() == utils.constants.STR_DEF:
#             return ['<str>']
#         elif calleeDefi.get_type() == utils.constants.LIST_DEF:
#             return ['<list>']
#         elif calleeDefi.get_type() == utils.constants.MAP_DEF:
#             return ['<map>']
#         else:
#             return [calleeNs]
#     # 正确匹配子字符串的指向并完成拼接
#     # def get_point(self,leftList:list,rightList: list,row=0):
#     def get_point(self,ns,row=0):
#         def helper(ns:str):
#             rightList = []
#             defi:Definition = self.def_manager.get(ns)
#             # while not defi or defi.get_type() in [utils.constants.NA_DEF,utils.constants.PARAM_DEF]:
#             while not defi or defi.get_type() in [utils.constants.NA_DEF, utils.constants.PARAM_DEF,
#                                                   utils.constants.RETURN_DEF]:
#                 rIndex = ns.rfind('.')
#                 if rIndex == -1:
#                     break
#                 rightList.insert(0,ns[rIndex:])
#                 ns = ns[:rIndex]
#                 defi = self.def_manager.get(ns)
#             rIndex = ns.rfind('.')
#             rightList.insert(0, ns[rIndex:])
#             ns = ns[:rIndex]
#             return [ns], rightList
#         if not isinstance(ns,str):
#             return []
#         leftList , rightList = helper(ns)
#         while rightList:
#             tmpList = []
#             leftList = list(map(lambda x :  NsRow(x.ns+rightList[0],x.row) if isinstance(x,NsRow) else NsRow(x+rightList[0],row),leftList))
#             rightList.remove(rightList[0])
#             leftList = list(map(self.convert,leftList))
#             # leftList = list(map(
#             #     lambda x: NsRow(x.ns + rightList[0], x.row) if isinstance(x, NsRow) else NsRow(x + rightList[0], row),
#             #     leftList))
#             # rightList.remove(rightList[0])
#             for left in leftList:
#                 tmpList += left
#             leftList = tmpList
#         # leftList = list(map(lambda x:NsRow(x,row) if isinstance(x,str) else x,leftList))
#         if not leftList:
#             return leftList
#         leftList = list(map(self.convert, leftList))
#         # leftList = list(reduce(operator ,leftList))
#         leftList = [i for item in leftList for i in item]
#         return leftList
#
#     # 将nsrow转换成最终的nsrow
#     def convert(self,nsrow:NsRow):
#         curStr = nsrow.ns
#         row = nsrow.row
#         curDefi: Definition = self.def_manager.get(curStr)
#         if not curDefi:
#             return [NsRow(curStr,row)]
#         if curDefi.get_type() in [utils.constants.NAME_DEF, utils.constants.NA_DEF]:
#             curDefiList, tmpRow = self.def_manager.get_final_pointName(curStr, row)
#             nsrowList = []
#             for curDefiNs in curDefiList:
#                 nsrowList.append(NsRow(curDefiNs,tmpRow))
#             return nsrowList
#         if curDefi.get_type() in [utils.constants.PARAM_DEF, utils.constants.RETURN_DEF]:
#             curDefiList, tmpRow = self.def_manager.get_final_pointName(curStr, row)
#             if curDefi.get_name() == 'self':
#                 tmpRow = row
#             nsrowList = []
#             for curDefiNs in curDefiList:
#                 nsrowList.append(NsRow(curDefiNs, tmpRow))
#             return nsrowList
#         if curDefi.get_type() == utils.constants.INT_DEF:
#             return [NsRow('<int>',row)]
#         if curDefi.get_type() == utils.constants.STR_DEF:
#             return [NsRow('<str>',row)]
#         if curDefi.get_type() == utils.constants.LIST_DEF:
#             return [NsRow('<list>',row)]
#         if curDefi.get_type() == utils.constants.MAP_DEF:
#             return [NsRow('<map>',row)]
#         # if curDefi.get_type() == utils.constants.CLS_DEF:
#         #     nsrowList = []
#         #     for clsNs in self.class_manager.get(curDefi.get_ns()).mro:
#         #         nsrowList.append(NsRow(clsNs,row))
#         #     return nsrowList
#         return [NsRow(curStr,row)]
#
#
#     # 完善scope
#     def complete_point(self,ns):
#         pass
#
#
#     # 1. 把params的point改变
#     def update(self,callNS:str, calleeScope:ScopeItem,callItem:CallItem , paramMap:dict):
#         callDefi:Definition = self.def_manager.get(callNS)
#         if callDefi and callDefi.get_type() in [utils.constants.IF_DEF, utils.constants.ELSE_DEF]:
#             def get_if_callns(ifScope:ScopeItem):
#                 ifDefi:Definition = self.def_manager.get(ifScope.get_ns())
#                 if ifDefi and ifDefi.get_type() not in [utils.constants.IF_DEF, utils.constants.ELSE_DEF]:
#                     return ifDefi.get_ns()
#                 else:
#                     return get_if_callns(ifScope.parent)
#             callNS = get_if_callns(self.scope_manager.get_scope(callNS))
#         if not isinstance(calleeScope ,ScopeItem):
#             return
#         # 根据defiNsOfFunc修改defiNs的point
#         def update_defi(defiNsOfFunc:str, defiNs:str, row):
#             if defiNs == ['bpytop.NetBox._draw_bg.<str>Download']:
#                 print()
#             # defiNsPointList = self.resolve(defiNs, row)
#             defiOfFunc: Definition = self.def_manager.get(defiNsOfFunc)
#             paramPrefixDefiList = calleeScope.get_prefix_defi(defiNsOfFunc)
#             if not paramPrefixDefiList:
#                 return
#             if isinstance(defiOfFunc,Definition) and not defiOfFunc.get_type() == utils.constants.PARAM_DEF:
#                 return
#             for paramPrefixDefi in paramPrefixDefiList:
#                 if paramPrefixDefi.get_ns() == defiNsOfFunc:
#                     continue
#                 suffix = utils.get_suffix(defiNsOfFunc , paramPrefixDefi.get_ns())
#                 paramPrefixDefiPointList = self.resolve(paramPrefixDefi.get_ns(),math.inf)
#                 # for defiNsPoint in defiNsPointList:
#                 if isinstance(defiNs , str):
#                     curNs = defiNs + suffix
#                     curDefi = self.def_manager.get(curNs)
#                     if not curDefi:
#                         curDefi:Definition = self.def_manager.create(curNs, utils.constants.NAME_DEF)
#                     elif curDefi.get_type() == utils.constants.NA_DEF:
#                         curDefi.def_type = utils.constants.NAME_DEF
#                     self.scope_manager.handle_assign(callNS, curNs.replace(callNS, '')[1:], curDefi)
#                     tmpCurDefiPoint = curDefi.add_name_point(callItem.row)
#                     for paramPrefixDefipointNs in paramPrefixDefiPointList:
#                         tmpCurDefiPoint.add(paramPrefixDefipointNs)
#                 elif isinstance(defiNs,list):
#                     defiNsList = defiNs
#                     for defiNs in defiNsList:
#                         curNs = defiNs + suffix
#                         curDefi = self.def_manager.get(curNs)
#                         if not curDefi:
#                             curDefi: Definition = self.def_manager.create(curNs, utils.constants.NAME_DEF)
#                         elif curDefi.get_type() == utils.constants.NA_DEF:
#                             curDefi.def_type = utils.constants.NAME_DEF
#                         self.scope_manager.handle_assign(callNS, curNs.replace(callNS, '')[1:], curDefi)
#                         tmpCurDefiPoint = curDefi.add_name_point(callItem.row)
#                         for paramPrefixDefipointNs in paramPrefixDefiPointList:
#                             tmpCurDefiPoint.add(paramPrefixDefipointNs)
#         # 如果被调用函数在调用函数的作用域中，内部操作会影响外部的变量
#         if self.isFather(callNS,calleeScope):
#             for key , value in paramMap.items():
#                 update_defi(key,value,callItem.row)
#             pass
#             for callDefiNs in self.scope_manager.get_scope(callNS).get_defs().copy():
#                 key = utils.join_ns(calleeScope.get_ns(),callDefiNs)
#                 value = self.scope_manager.get_def(callNS,callDefiNs).get_ns()
#                 update_defi(key,value,callItem.row)
#         # 外部函数，只需要更新params
#         else:
#             for key , value in paramMap.items():
#                 update_defi(key,value,callItem.row)
#         calleeDefi = self.def_manager.get(calleeScope.get_ns())
#         if calleeDefi and calleeDefi.get_type() == utils.constants.FUN_DEF:
#             self.call_graph.add_edge(callNS, calleeScope.get_ns())
#         # self.call_graph.add_edge(callNS, calleeScope.get_ns())
#
#     # 调用函数是不是被调用函数的parent，用到并查集
#     def isFather(self,callNs:str,calleeScope:ScopeItem):
#         while calleeScope:
#             if calleeScope.get_ns() == callNs:
#                 return True
#             calleeScope = calleeScope.parent
#         return False
#
#     def get_modules_analyzed(self):
#         return set()
#
#     # 现将参数解析到正确的defi，然后在匹配
#     # 将传递的参数和scope的参数匹配起来
#     def match_params(self,calleeNs,item:CallItem) -> dict:
#         calleeScope:ScopeItem = self.scope_manager.get_scope(calleeNs)
#         if not calleeScope:
#             return
#         paramsMap = {}
#         scopeParamList = calleeScope.params
#         for index,param in enumerate(item.params):
#             if index >= len(scopeParamList):
#                 break
#             if isinstance(param,str):
#                 paramsMap[scopeParamList[index].get_ns()] = param
#             elif isinstance(param,dict):
#                 for k,v in param.items():
#                     paramsMap[utils.join_ns(calleeNs,k)] = v
#         for declaredParam , callParam in paramsMap.items():
#             declaredParamDefi:Definition = self.def_manager.get(declaredParam)
#             if not declaredParamDefi or not declaredParamDefi.get_type() == utils.constants.PARAM_DEF:
#                 continue
#             # callParamPoints = self.resolve(callParam,item.row)
#             if isinstance(callParam,list):
#                 callParamPoints = map(lambda x:self.resolve(x,item.row) , callParam)
#                 callParamPoints = reduce(lambda x,y : x+y , callParamPoints)
#             elif isinstance(callParam,str):
#                 callParamPoints = self.resolve(callParam, item.row)
#             moduleNs = self.get_module_ns(calleeNs)
#             if calleeNs == 'distutils.util.convert_path':
#                 print()
#             method = self.module_manager.get_func_name(moduleNs,calleeNs)
#             if not method and calleeNs.endswith("__init__"):
#                 method = self.module_manager.get_func_name(moduleNs, calleeNs.replace("." + utils.constants.CLS_INIT, ''))
#             tmp = declaredParamDefi.add_name_point(row=method['first'])
#             for pointItem in callParamPoints:
#                 tmp.add(pointItem)
#         return paramsMap
#
#     def call(self,callNs , calleeNs:str , callItem:CallItem):
#         print(callNs,calleeNs)
#         tmpstr = "bpytop.process_keys bpytop.Collector.collect_done.wait"
#         if callNs == tmpstr.split(" ")[0] and calleeNs == tmpstr.split(" ")[1]:
#             print()
#
#         tmpstr = "hmac.HMAC.__init__ hmac.HMAC.__init__.key.ljust.<RETURN>.ljust"
#         calleeScope: ScopeItem = self.scope_manager.get_scope(calleeNs)
#         if not calleeScope:
#             callDefi: Definition = self.def_manager.get(callNs)
#             if callDefi and callDefi.get_type() in [utils.constants.IF_DEF, utils.constants.ELSE_DEF]:
#                 callNs = self.get_if_callns(self.scope_manager.get_scope(callNs))
#             calleedefi:Definition = self.def_manager.get(calleeNs)
#             if calleedefi or calleeNs.startswith("<"):
#                 self.call_graph.add_edge(callNs, calleeNs)
#             # self.call_graph.add_edge(callNs, calleeNs)
#             return
#         calleeNs = calleeScope.get_ns()
#         copyScope = copy.deepcopy(calleeScope)
#         # 完成参数匹配。如果是类函数，需要添加一个self参数
#         parentScopeItem = calleeScope.parent
#         parentDefi:Definition = self.def_manager.get(parentScopeItem.get_ns())
#         flag = False
#         if parentDefi and parentDefi.get_type() == utils.constants.CLS_DEF:
#             flag = True
#             if calleeNs.endswith(utils.constants.CLS_INIT):
#                 copyClassScopeItemNs = self.copy_class(callNs,parentDefi.get_ns())
#                 # copyClassScopeItemNs = calleeNs
#                 if not callItem.inheritt:
#                     # copyClassScopeItemNs = calleeNs
#                     callItem.params.insert(0,copyClassScopeItemNs)
#                 else:
#                     seq = self.scope_manager.get_seq(callNs)
#                     if seq == 0:
#                         insertNs = callNs
#                     else:
#                         insertNs = utils.join_ns(callNs[:callNs.rfind(".")],utils.get_scope_copy_name(seq))
#                     callItem.params.insert(0,insertNs)
#                     # callItem.params.insert(0,'...micro-benchmark.snippets.classes.super_class_return.main.B.<copy1>')
#             else:
#                 #拿到self
#                 # callItem.params.insert(0,self.get_attr_ns(callItem.func_name))
#                 callItem.params.insert(0,self.resolve(self.get_attr_ns(callItem.func_name),callItem.row)[0])
#                 pass
#         paramsMap = self.match_params(calleeNs,callItem)
#         # 完成pfg的更新
#         # self.call_graph.add_edge(callNs, calleeScope.get_ns())
#         calleeScope = self.dfs(calleeNs,callItem)
#         self.update(callNs,calleeScope,callItem,paramsMap)
#         # # 进行return的匹配
#         self.match_return(callNs,callItem)
#         self.reset_scope(calleeScope,copyScope,callNs)
#         if flag:
#             callItem.params.remove(callItem.params[0])
#         pass
#
#     def match_return(self,callNs,callItem:CallItem):
#         def match(left , right):
#             leftDefi:Definition = self.def_manager.get(left)
#             rightDefi:Definition = self.def_manager.get(right)
#             tmpRightDefi = rightDefi
#             # rightList = self.resolve(right,callItem.row+1)
#             rightScope = self.get_scope_ns(right)
#             self.def_manager.get_defs()[right] = self.scope_manager.get_scope(rightScope).get_def(
#                 utils.constants.RETURN_NAME)
#             rightList = self.resolve(right,callItem.row+1)
#             self.def_manager.get_defs()[right] = tmpRightDefi
#             tmpList = []
#             for pointReturnDefiNs in rightList:
#                 pointReturnDefi: Definition = self.def_manager.get(pointReturnDefiNs)
#                 if not pointReturnDefi:
#                     break
#                 if pointReturnDefi.get_type() not in [utils.constants.NAME_DEF, utils.constants.FUN_DEF,
#                                                       utils.constants.CLS_DEF, utils.constants.EXT_DEF]:
#                     break
#                 tmpList.append(pointReturnDefiNs)
#             tmpPoint = leftDefi.add_name_point(callItem.row)
#             for tmp in tmpList:
#                 tmpPoint.add(tmp)
#             leftDefi.def_type = utils.constants.NAME_DEF
#         curReturnDefiNs = utils.join_ns(callItem.func_name, utils.constants.RETURN_NAME)
#         curReturnDefi:Definition = self.def_manager.get(curReturnDefiNs)
#         if not curReturnDefi:
#             curReturnDefi = self.def_manager.create(curReturnDefiNs, utils.constants.RETURN_DEF)
#         # pointReturnDefiNsList = self.resolve(curReturnDefiNs,callItem.row)
#         # if not curReturnDefiNs in pointReturnDefiNsList:
#         #     tmp = curReturnDefi.add_name_point(callItem.row)
#         #     for point in pointReturnDefiNsList:
#         #         tmp.add(point)
#         leftName = self.return_manager.pop_returnItem(callItem.ns,callItem.row,callItem.func_name)
#         if not leftName:
#             leftName = curReturnDefiNs
#         match(leftName,curReturnDefiNs)
#         pass
#
#
#     # 将scope复原，同时defi也复原
#     def reset_scope(self,scope:ScopeItem,copyScope:ScopeItem,callNs = None):
#         for defi in copyScope.get_defs():
#             if defi.endswith(utils.constants.RETURN_NAME) and (callNs and callNs in scope.get_ns()):
#                 continue
#             self.def_manager.get_defs()[copyScope.get_def(defi).get_ns()] = copyScope.get_def(defi)
#         self.scope_manager.get_scopes()[scope.get_ns()] = copyScope
#
#     # 复制scope首先复制defi
#     def copy_scope(self , scopeItemNs:str , copyScopeItemNS:str,originNs):
#         # copy scope
#         # print(scopeItemNs,copyScopeItemNS)
#         if self.scope_manager.get_scope(copyScopeItemNS):
#             return
#         curScopeItem: ScopeItem = self.scope_manager.get_scope(scopeItemNs)
#         curDefi = self.def_manager.get(scopeItemNs)
#         copyDefi:Definition = copy.deepcopy(curDefi)
#         self.def_manager.get_defs()[copyScopeItemNS] = copyDefi
#         for point in copyDefi.points:
#             point.points_to = set(map(lambda x:x.replace(originNs,self.classMap[originNs]) , point.points_to))
#         if curScopeItem:
#             copyScopeItem = copy.deepcopy(curScopeItem)
#             self.scope_manager.get_scopes()[copyScopeItemNS] = copyScopeItem
#             for ns , defi in copyScopeItem.get_defs().items():
#                 self.copy_scope(defi.get_ns() , utils.join_ns(copyScopeItemNS,ns),originNs)
#     # copy class-scope
#     def copy_class(self ,callNs, classScopeNs:str):
#         # copyClassScopeNs = utils.join_ns(callNs , classScopeNs.split(".")[-1],utils.get_scope_copy_name(self.scope_manager.get_seq()))
#         copyClassScopeNs = utils.join_ns(classScopeNs,utils.get_scope_copy_name(self.scope_manager.add_seq(callNs)))
#         if not hasattr(self ,"classMap"):
#             self.classMap = {}
#         self.classMap[classScopeNs] = copyClassScopeNs
#         self.copy_scope(classScopeNs, copyClassScopeNs, classScopeNs)
#
#         return copyClassScopeNs
#
#
#     def get_attr_ns(self,ns:str):
#         return utils.join_ns(*ns.split('.')[:-1])
#
#     def get_scope_ns(self,ns):
#         while not ns in self.scope_manager.get_scopes():
#             ns = ns[:ns.rfind(".")]
#         return ns
#
#     def get_module_ns(self,ns):
#         defi:Definition = self.def_manager.get(ns)
#         while not defi or defi.get_type() != utils.constants.MOD_DEF :
#             ns = ns[:ns.rfind(".")]
#             defi = self.def_manager.get(ns)
#         return ns
#
#     def get_if_callns(self,ifScope: ScopeItem):
#         ifDefi: Definition = self.def_manager.get(ifScope.get_ns())
#         if ifDefi and ifDefi.get_type() not in [utils.constants.IF_DEF, utils.constants.ELSE_DEF]:
#             return ifDefi.get_ns()
#         else:
#             return self.get_if_callns(ifScope.parent)
#

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


class NsRow:
    def __init__(self, ns, row):
        self.ns = ns
        self.row = row


class CallGraphProcessor():
    def __init__(self, input_file, input_mod,
                 scope_manager, def_manager, class_manager,
                 module_manager, call_manager, call_graph, return_manager, modules_analyzed=None):
        self.input_file = input_file
        self.input_mod = input_mod
        self.module_analyzed = modules_analyzed
        self.scope_manager: ScopeManager = scope_manager
        self.def_manager: DefinitionManager = def_manager
        self.class_manager = class_manager
        self.module_manager: ModuleManager = module_manager
        self.call_graph: CallGraph = call_graph
        self.call_manager: call_manager = call_manager
        self.format = set()
        self.return_manager: ReturnManager = return_manager
        self.selfMap = {}
        self.calledFuncSet: set = set()
        self.calledScope = {}

    def analyze(self):
        self.get_call_graph()

    def get_all_reachable_functions(self):
        reachable = set()
        names = set()
        current_scope = self.scope_manager.get_scope(self.current_ns)
        while current_scope:
            for name, defi in current_scope.get_defs().items():
                if defi.is_function_def() and not name in names:
                    closured = self.closured.get(defi.get_ns())
                    for item in closured:
                        reachable.add(item)
                    names.add(name)
            current_scope = current_scope.parent

        return reachable

    def has_ext_parent(self, node):
        if not isinstance(node, ast.Attribute):
            return False

        while isinstance(node, ast.Attribute):
            parents = self._retrieve_parent_names(node)
            for parent in parents:
                for name in self.closured.get(parent, []):
                    defi = self.def_manager.get(name)
                    if defi and defi.is_ext_def():
                        return True
            node = node.value
        return False

    def get_full_attr_names(self, node):
        name = ""
        while isinstance(node, ast.Attribute):
            if not name:
                name = node.attr
            else:
                name = node.attr + "." + name
            node = node.value

        names = []
        if getattr(node, "id", None) == None:
            return names

        defi = self.scope_manager.get_def(self.current_ns, node.id)
        if defi and self.closured.get(defi.get_ns()):
            for id in self.closured.get(defi.get_ns()):
                names.append(id + "." + name)
        return names

    def is_builtin(self, name):
        return name in __builtins__

    # 返回函数的scope，还需要加上参数
    def dfs(self, callNs: str, item: CallItem = None) -> ScopeItem:
        # 如果这个方法没有解析，直接返回
        curScope = self.scope_manager.get_scope(callNs)
        if not curScope:
            return callNs
        if str(curScope) in self.calledScope:
            return self.calledScope[str(curScope)]
        curDefi: Definition = self.def_manager.get(callNs)
        if curDefi.get_type() not in [utils.constants.IF_DEF, utils.constants.ELSE_DEF]:
            self.call_graph.add_node(callNs)
        callItemList = self.call_manager.get(callNs)
        # 将函数匹配起来
        if not callItemList:
            return self.scope_manager.get_scope(callNs)
        for callItem in callItemList:
            defi: Definition = self.def_manager.get(callItem.func_name)
            if defi and defi.get_type() in [utils.constants.IF_DEF]:
                self.call_if(callNs, callItem)
                continue
            if "|||" in callItem.func_name:
                self.call_else(callNs, callItem)
                continue
            calleeNsList = self.resolve(callItem.func_name, callItem.row + 1, True)
            for calleeNs in calleeNsList:
                if calleeNs not in self.calledFuncSet:
                    # if callNs == 'macro_benchmark.noDecy.bpytop.bpytop.Config.load_config' and calleeNs == '<builtin>.open':
                    #     print()
                    self.calledFuncSet.add(calleeNs)
                    self.call(callNs, calleeNs, callItem)
                    self.calledFuncSet.remove(calleeNs)
        self.calledScope[str(curScope)] = copy.deepcopy(curScope)
        return curScope

    def call_if(self, callNs, callItem: CallItem):
        calleeNs = callItem.func_name
        calleeScope: ScopeItem = self.scope_manager.get_scope(calleeNs)
        calleeNs = calleeScope.get_ns()
        copyScope = copy.deepcopy(calleeScope)
        # 完成pfg的更新
        calleeScope = self.dfs(calleeNs, callItem)
        # self.match_return(callNs, callItem)
        self.update_if(callNs, calleeScope, callItem)
        self.reset_scope(calleeScope, copyScope)
        pass

    def update_if(self, callNs: str, calleeScope: ScopeItem, callItem: CallItem):
        for defiNs, defi in calleeScope.get_defs().items():
            curDefiNs = utils.join_ns(callNs, defiNs)
            curDefi: Definition = self.def_manager.get(curDefiNs)
            if not curDefi:
                curDefi = self.def_manager.create(curDefiNs, utils.constants.NAME_DEF)
            pointNsList = self.resolve(utils.join_ns(calleeScope.get_ns(), defiNs), math.inf)
            tmpPoint = curDefi.add_name_point(callItem.row)
            for point in pointNsList:
                tmpPoint.add(point)
        pass

    def call_else(self, callNs, callItem: CallItem):
        calleeNsList = callItem.func_name.split("|||")
        calleeIf, calleeElse = calleeNsList
        callifScope: ScopeItem = self.scope_manager.get_scope(calleeIf)
        callelseScope: ScopeItem = self.scope_manager.get_scope(calleeElse)
        callifNs = callifScope.get_ns()
        callelseNs = callelseScope.get_ns()
        copyIfScope = copy.deepcopy(callifScope)
        copyElseScope = copy.deepcopy(callelseScope)
        # 完成pfg的更新
        callifScope = self.dfs(callifNs, callItem)
        callelseScope = self.dfs(callelseNs, callItem)
        self.merge_if_else(callifScope, callelseScope)
        self.update_if(callNs, callelseScope, callItem)
        self.reset_scope(callifScope, copyIfScope)
        self.reset_scope(callelseScope, copyElseScope)
        pass

    def merge_if_else(self, ifScope: ScopeItem, elseScope: ScopeItem):
        elseScopeNs = elseScope.get_ns()
        for defiNs, defi in ifScope.get_defs().items():
            elseDefiNs = utils.join_ns(elseScopeNs, defiNs)
            elseDefi: Definition = self.def_manager.get(elseDefiNs)
            if not elseDefi:
                elseDefi = defi
                self.scope_manager.handle_assign(elseScope.get_ns(), elseDefiNs.replace(elseScope.get_ns(), '')[1:],
                                                 elseDefi)
            else:
                pointNsList = self.resolve(utils.join_ns(ifScope.get_ns(), defiNs), math.inf)
                tmpElsePoint = elseDefi.get_last_point()
                if not tmpElsePoint:
                    return
                for point in pointNsList:
                    tmpElsePoint.points_to.add(point)
        pass

    def get_call_graph(self):
        for callNs in self.def_manager.entrySet:
            if callNs not in self.call_graph.cg:
                self.dfs(callNs)


    # 将calleeNS转变成真正的指向
    def resolve(self, calleeNs: str, row: int, flag=False) -> list:
        if not isinstance(calleeNs, str):
            return []
        calleeDefi: Definition = self.def_manager.get(calleeNs)
        if not calleeDefi or calleeDefi.get_type() in [utils.constants.NAME_DEF, utils.constants.NA_DEF,
                                                       utils.constants.PARAM_DEF, utils.constants.RETURN_DEF]:
            # nsRowList = self.get_point([''], self.convectStrtoList(calleeNs), row)
            nsRowList = self.get_point(calleeNs, row)
            for nsRow in nsRowList:
                if nsRow.ns == calleeNs:
                    return list(map(lambda x: x.ns, nsRowList))
                if calleeNs in nsRow.ns:
                    return list(map(lambda x: x.ns, nsRowList))
            returnDefiNsList = []
            for nsRow in nsRowList:
                defiList = self.resolve(nsRow.ns, nsRow.row, flag)
                returnDefiNsList += defiList
            return returnDefiNsList
        if not calleeDefi:
            return [calleeNs]
        if calleeDefi.get_type() in [utils.constants.FUN_DEF, utils.constants.EXT_DEF]:
            return [calleeNs]
        if calleeDefi.get_type() == utils.constants.CLS_DEF:
            return [utils.join_ns(calleeNs, utils.constants.CLS_INIT)] if flag else [calleeNs]
        elif calleeDefi.get_type() == utils.constants.INT_DEF:
            return ['<int>']
        elif calleeDefi.get_type() == utils.constants.STR_DEF:
            return ['<str>']
        elif calleeDefi.get_type() == utils.constants.LIST_DEF:
            return ['<list>']
        elif calleeDefi.get_type() == utils.constants.MAP_DEF:
            return ['<dict>']
        else:
            return [calleeNs]

    # 正确匹配子字符串的指向并完成拼接
    def get_point(self, ns, row=0):
        def helper(ns: str):
            rightList = []
            defi: Definition = self.def_manager.get(ns)
            # while not defi or defi.get_type() in [utils.constants.NA_DEF,utils.constants.PARAM_DEF]:
            while not defi or defi.get_type() in [utils.constants.NA_DEF, utils.constants.PARAM_DEF,
                                                  utils.constants.RETURN_DEF]:
                rIndex = ns.rfind('.')
                if rIndex == -1:
                    break
                rightList.insert(0, ns[rIndex:])
                ns = ns[:rIndex]
                defi = self.def_manager.get(ns)
            rIndex = ns.rfind('.')
            rightList.insert(0, ns[rIndex:])
            ns = ns[:rIndex]
            return [ns], rightList

        if not isinstance(ns, str):
            return []
        leftList, rightList = helper(ns)
        while rightList:
            tmpList = []
            leftList = list(
                map(lambda x: NsRow(x.ns + rightList[0], x.row) if isinstance(x, NsRow) else NsRow(x + rightList[0],
                                                                                                   row), leftList))
            rightList.remove(rightList[0])
            leftList = list(map(self.convert, leftList))
            for left in leftList:
                tmpList += left
            leftList = tmpList
        if not leftList:
            return leftList
        leftList = list(map(self.convert, leftList))
        leftList = [i for item in leftList for i in item]
        return leftList

    # 将nsrow转换成最终的nsrow
    def convert(self, nsrow: NsRow):
        curStr = nsrow.ns
        row = nsrow.row
        curDefi: Definition = self.def_manager.get(curStr)
        if not curDefi:
            return [NsRow(curStr, row)]
        if curDefi.get_type() in [utils.constants.NAME_DEF, utils.constants.NA_DEF]:
            curDefiList, tmpRow = self.def_manager.get_final_pointName(curStr, row)
            nsrowList = []
            for curDefiNs in curDefiList:
                nsrowList.append(NsRow(curDefiNs, tmpRow))
            return nsrowList
        if curDefi.get_type() in [utils.constants.PARAM_DEF, utils.constants.RETURN_DEF]:
            curDefiList, tmpRow = self.def_manager.get_final_pointName(curStr, row)
            if curDefi.get_name() == 'self':
                tmpRow = row
            nsrowList = []
            for curDefiNs in curDefiList:
                nsrowList.append(NsRow(curDefiNs, tmpRow))
            return nsrowList
        if curDefi.get_type() == utils.constants.INT_DEF:
            return [NsRow('<int>', row)]
        if curDefi.get_type() == utils.constants.STR_DEF:
            return [NsRow('<str>', row)]
        if curDefi.get_type() == utils.constants.LIST_DEF:
            return [NsRow('<list>', row)]
        if curDefi.get_type() == utils.constants.MAP_DEF:
            return [NsRow('<map>', row)]
        return [NsRow(curStr, row)]

    # 完善scope
    def complete_point(self, ns):
        pass

    # 1. 把params的point改变
    def update(self, callNS: str, calleeScope: ScopeItem, callItem: CallItem, paramMap: dict):
        callDefi: Definition = self.def_manager.get(callNS)
        if callDefi and callDefi.get_type() in [utils.constants.IF_DEF, utils.constants.ELSE_DEF]:
            def get_if_callns(ifScope: ScopeItem):
                ifDefi: Definition = self.def_manager.get(ifScope.get_ns())
                if ifDefi and ifDefi.get_type() not in [utils.constants.IF_DEF, utils.constants.ELSE_DEF]:
                    return ifDefi.get_ns()
                else:
                    return get_if_callns(ifScope.parent)

            callNS = get_if_callns(self.scope_manager.get_scope(callNS))
        if not isinstance(calleeScope, ScopeItem):
            return

        # 根据defiNsOfFunc修改defiNs的point
        def update_defi(defiNsOfFunc: str, defiNs: str, row):
            # defiNsPointList = self.resolve(defiNs, row)
            defiOfFunc: Definition = self.def_manager.get(defiNsOfFunc)
            paramPrefixDefiList = calleeScope.get_prefix_defi(defiNsOfFunc)
            if not paramPrefixDefiList:
                return
            if isinstance(defiOfFunc, Definition) and not defiOfFunc.get_type() == utils.constants.PARAM_DEF:
                return
            for paramPrefixDefi in paramPrefixDefiList:
                if paramPrefixDefi.get_ns() == defiNsOfFunc:
                    continue
                suffix = utils.get_suffix(defiNsOfFunc, paramPrefixDefi.get_ns())
                paramPrefixDefiPointList = self.resolve(paramPrefixDefi.get_ns(), math.inf)
                # for defiNsPoint in defiNsPointList:
                if isinstance(defiNs, str):
                    curNsList = [defiNs + suffix]
                elif isinstance(defiNs, list):
                    curNsList = list(map(lambda x: x + suffix, defiNs))
                for curNs in curNsList:
                    curDefi = self.def_manager.get(curNs)
                    if not curDefi:
                        curDefi: Definition = self.def_manager.create(curNs, utils.constants.NAME_DEF)
                    elif curDefi.get_type() == utils.constants.NA_DEF:
                        curDefi.def_type = utils.constants.NAME_DEF
                    self.scope_manager.handle_assign(callNS, curNs.replace(callNS, '')[1:], curDefi)
                    tmpCurDefiPoint = curDefi.add_name_point(callItem.row)
                    for paramPrefixDefipointNs in paramPrefixDefiPointList:
                        tmpCurDefiPoint.add(paramPrefixDefipointNs)
                # for defiNsPoint in defiNsPointList:
                #     curNs = defiNsPoint + suffix
                #     curDefi = self.def_manager.get(curNs)
                #     if not curDefi:
                #         curDefi = self.def_manager.create(curNs, utils.constants.NAME_DEF)
                #     elif curDefi.get_type() == utils.constants.NA_DEF:
                #         curDefi.def_type = utils.constants.NAME_DEF
                #     self.scope_manager.handle_assign(callNS, curNs.replace(callNS, '')[1:], curDefi)
                #     curDefi.merge(paramPrefixDefi, callItem.row)
                # curNs = defiNs + suffix
                # curDefi = self.def_manager.get(curNs)
                # if not curDefi:
                #     curDefi = self.def_manager.create(curNs, utils.constants.NAME_DEF)
                # elif curDefi.get_type() == utils.constants.NA_DEF:
                #     curDefi.def_type = utils.constants.NAME_DEF
                # self.scope_manager.handle_assign(callNS, curNs.replace(callNS, '')[1:], curDefi)
                # curDefi.merge(paramPrefixDefi, callItem.row)

        # 如果被调用函数在调用函数的作用域中，内部操作会影响外部的变量
        if self.isFather(callNS, calleeScope):
            for key, value in paramMap.items():
                update_defi(key, value, callItem.row)
            pass
            for callDefiNs in self.scope_manager.get_scope(callNS).get_defs().copy():
                key = utils.join_ns(calleeScope.get_ns(), callDefiNs)
                value = self.scope_manager.get_def(callNS, callDefiNs).get_ns()
                update_defi(key, value, callItem.row)
        # 外部函数，只需要更新params
        else:
            for key, value in paramMap.items():
                update_defi(key, value, callItem.row)
        calleeDefi = self.def_manager.get(calleeScope.get_ns())
        if calleeDefi and calleeDefi.get_type() == utils.constants.FUN_DEF:
            self.call_graph.add_edge(callNS, calleeScope.get_ns())
        self.call_graph.add_edge(callNS, calleeScope.get_ns())

    # 调用函数是不是被调用函数的parent，用到并查集
    def isFather(self, callNs: str, calleeScope: ScopeItem):
        while calleeScope:
            if calleeScope.get_ns() == callNs:
                return True
            calleeScope = calleeScope.parent
        return False

    def get_modules_analyzed(self):
        return set()

    # 现将参数解析到正确的defi，然后在匹配
    # 将传递的参数和scope的参数匹配起来
    def match_params(self, calleeNs, item: CallItem) -> dict:
        calleeScope: ScopeItem = self.scope_manager.get_scope(calleeNs)
        if not calleeScope:
            return
        paramsMap = {}
        scopeParamList = calleeScope.params
        for index, param in enumerate(item.params):
            if index >= len(scopeParamList):
                break
            if isinstance(param, str):
                paramsMap[scopeParamList[index].get_ns()] = param
            elif isinstance(param, dict):
                for k, v in param.items():
                    if not k:
                        continue
                    paramsMap[utils.join_ns(calleeNs, k)] = v
        for declaredParam, callParam in paramsMap.items():
            declaredParamDefi: Definition = self.def_manager.get(declaredParam)
            if not declaredParamDefi or not declaredParamDefi.get_type() == utils.constants.PARAM_DEF:
                continue
            if isinstance(callParam, str):
                callParamPoints = self.resolve(callParam, item.row)
            elif isinstance(callParam, list) and callParam:
                callParamPoints = list(map(lambda x: self.resolve(x, row=item.row), callParam))
                callParamPoints = reduce(lambda x, y: x + y, callParamPoints)
            moduleNs = self.get_module_ns(calleeNs)
            method = self.module_manager.get_func_name(moduleNs, calleeNs)
            if not method and calleeNs.endswith("__init__"):
                method = self.module_manager.get_func_name(moduleNs,
                                                           calleeNs.replace("." + utils.constants.CLS_INIT, ''))
            tmp = declaredParamDefi.add_name_point(row=method['first'])
            for pointItem in callParamPoints:
                tmp.add(pointItem)
        return paramsMap

    def call(self, callNs, calleeNs: str, callItem: CallItem):
        calleeScope: ScopeItem = self.scope_manager.get_scope(calleeNs)
        # print(callNs , "调用了" , calleeNs)
        if not calleeScope:
            callDefi: Definition = self.def_manager.get(callNs)
            if callDefi and callDefi.get_type() in [utils.constants.IF_DEF, utils.constants.ELSE_DEF]:
                def get_if_callns(ifScope: ScopeItem):
                    ifDefi: Definition = self.def_manager.get(ifScope.get_ns())
                    if ifDefi and ifDefi.get_type() not in [utils.constants.IF_DEF, utils.constants.ELSE_DEF]:
                        return ifDefi.get_ns()
                    else:
                        return get_if_callns(ifScope.parent)

                callNs = get_if_callns(self.scope_manager.get_scope(callNs))
            calleeDefi = self.def_manager.get(calleeNs)
            if not calleeDefi and calleeNs.startswith("<"):
                self.call_graph.add_edge(callNs, calleeNs)
            elif calleeDefi and calleeDefi.get_type() in [utils.constants.NA_DEF, utils.constants.PARAM_DEF]:
                return
            elif calleeDefi:
                self.call_graph.add_edge(callNs, calleeNs)
            # self.call_graph.add_edge(callNs, calleeNs)
            return
        calleeNs = calleeScope.get_ns()
        copyScope = copy.deepcopy(calleeScope)
        # 完成参数匹配。如果是类函数，需要添加一个self参数
        parentScopeItem = calleeScope.parent
        parentDefi: Definition = self.def_manager.get(parentScopeItem.get_ns())
        flag = False
        if parentDefi and parentDefi.get_type() == utils.constants.CLS_DEF:
            flag = True
            if calleeNs.endswith(utils.constants.CLS_INIT):
                copyClassScopeItemNs = self.copy_class(callNs, parentDefi.get_ns())
                # copyClassScopeItemNs = calleeNs
                if not callItem.inheritt:
                    # copyClassScopeItemNs = calleeNs
                    callItem.params.insert(0, copyClassScopeItemNs)
                else:
                    seq = self.scope_manager.get_seq(callNs)
                    if seq == 0:
                        insertNs = callNs
                    else:
                        insertNs = utils.join_ns(callNs[:callNs.rfind(".")], utils.get_scope_copy_name(seq))
                    callItem.params.insert(0, insertNs)
            else:
                # 拿到self
                # callItem.params.insert(0,self.get_attr_ns(callItem.func_name))
                callItem.params.insert(0, self.resolve(self.get_attr_ns(callItem.func_name), callItem.row)[0])
                pass
        paramsMap = self.match_params(calleeNs, callItem)
        # 完成pfg的更新
        # self.call_graph.add_edge(callNs, calleeScope.get_ns())
        calleeScope = self.dfs(calleeNs, callItem)
        self.update(callNs, calleeScope, callItem, paramsMap)
        # # 进行return的匹配
        self.match_return(callNs, callItem)
        self.reset_scope(calleeScope, copyScope, callNs)
        if flag:
            callItem.params.remove(callItem.params[0])
        pass

    def match_return(self, callNs, callItem: CallItem):
        def match(left, right):
            leftDefi: Definition = self.def_manager.get(left)
            rightDefi: Definition = self.def_manager.get(right)
            tmpRightDefi = rightDefi
            # rightList = self.resolve(right,callItem.row+1)
            rightScope = self.get_scope_ns(right)
            self.def_manager.get_defs()[right] = self.scope_manager.get_scope(rightScope).get_def(
                utils.constants.RETURN_NAME)
            rightList = self.resolve(right, callItem.row + 1)
            self.def_manager.get_defs()[right] = tmpRightDefi
            tmpList = []
            for pointReturnDefiNs in rightList:
                pointReturnDefi: Definition = self.def_manager.get(pointReturnDefiNs)
                if not pointReturnDefi:
                    break
                if pointReturnDefi.get_type() not in [utils.constants.NAME_DEF, utils.constants.FUN_DEF,
                                                      utils.constants.CLS_DEF, utils.constants.EXT_DEF]:
                    break
                tmpList.append(pointReturnDefiNs)
            tmpPoint = leftDefi.add_name_point(callItem.row)
            for tmp in tmpList:
                tmpPoint.add(tmp)
            leftDefi.def_type = utils.constants.NAME_DEF

        curReturnDefiNs = utils.join_ns(callItem.func_name, utils.constants.RETURN_NAME)
        curReturnDefi: Definition = self.def_manager.get(curReturnDefiNs)
        if not curReturnDefi:
            curReturnDefi = self.def_manager.create(curReturnDefiNs, utils.constants.RETURN_DEF)
        # pointReturnDefiNsList = self.resolve(curReturnDefiNs,callItem.row)
        # if not curReturnDefiNs in pointReturnDefiNsList:
        #     tmp = curReturnDefi.add_name_point(callItem.row)
        #     for point in pointReturnDefiNsList:
        #         tmp.add(point)
        leftName = self.return_manager.pop_returnItem(callItem.ns, callItem.row, callItem.func_name)
        if not leftName:
            leftName = curReturnDefiNs
        match(leftName, curReturnDefiNs)
        pass

    # 将scope复原，同时defi也复原
    def reset_scope(self, scope: ScopeItem, copyScope: ScopeItem, callNs=None):
        for defi in copyScope.get_defs():
            if defi.endswith(utils.constants.RETURN_NAME) and (callNs and callNs in scope.get_ns()):
                continue
            self.def_manager.get_defs()[copyScope.get_def(defi).get_ns()] = copyScope.get_def(defi)
        self.scope_manager.get_scopes()[scope.get_ns()] = copyScope

    # 复制scope首先复制defi
    def copy_scope(self, scopeItemNs: str, copyScopeItemNS: str, originNs):
        # copy scope
        # print(scopeItemNs,copyScopeItemNS)
        if self.scope_manager.get_scope(copyScopeItemNS):
            return
        curScopeItem: ScopeItem = self.scope_manager.get_scope(scopeItemNs)
        curDefi = self.def_manager.get(scopeItemNs)
        copyDefi: Definition = copy.deepcopy(curDefi)
        self.def_manager.get_defs()[copyScopeItemNS] = copyDefi
        for point in copyDefi.points:
            point.points_to = set(map(lambda x: x.replace(originNs, self.classMap[originNs]), point.points_to))
        if curScopeItem:
            copyScopeItem = copy.deepcopy(curScopeItem)
            self.scope_manager.get_scopes()[copyScopeItemNS] = copyScopeItem
            for ns, defi in copyScopeItem.get_defs().items():
                self.copy_scope(defi.get_ns(), utils.join_ns(copyScopeItemNS, ns), originNs)

    # copy class-scope
    def copy_class(self, callNs, classScopeNs: str):
        # copyClassScopeNs = utils.join_ns(callNs , classScopeNs.split(".")[-1],utils.get_scope_copy_name(self.scope_manager.get_seq()))
        copyClassScopeNs = utils.join_ns(classScopeNs, utils.get_scope_copy_name(self.scope_manager.add_seq(callNs)))
        if not hasattr(self, "classMap"):
            self.classMap = {}
        self.classMap[classScopeNs] = copyClassScopeNs
        self.copy_scope(classScopeNs, copyClassScopeNs, classScopeNs)

        return copyClassScopeNs

    def get_attr_ns(self, ns: str):
        return utils.join_ns(*ns.split('.')[:-1])

    def get_scope_ns(self, ns):
        while not ns in self.scope_manager.get_scopes():
            ns = ns[:ns.rfind(".")]
        return ns

    def get_module_ns(self, ns):
        defi: Definition = self.def_manager.get(ns)
        while not defi or defi.get_type() != utils.constants.MOD_DEF:
            ns = ns[:ns.rfind(".")]
            defi = self.def_manager.get(ns)
        return ns
