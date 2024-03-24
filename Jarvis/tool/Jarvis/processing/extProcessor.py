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

import ast
from machinery.definitions import (
    Definition,
    DefinitionManager,
    ChangeManager,
    ChangeItem,
)
from machinery.classes import ClassManager, ClassNode
from machinery.scopes import ScopeManager, ScopeItem
from processing.base import ProcessingBase
from machinery.imports import ImportManager
from machinery.nodes import NodeManager
from machinery.modules import ModuleManager, Module
from machinery import gol

import utils
from functools import reduce
from machinery.callgraph import CallGraph


class ExtProcessor(ProcessingBase):
    def __init__(
            self,
            filename,
            modname,
            import_manager,
            scope_manager,
            def_manager,
            class_manager,
            module_manager,
            change_manager,
            node_manager,
            cg,
            callStack=[],
            visited_scope=set(),
            modules_analyzed=None,
            decy=True,
    ):
        if filename.endswith(".so") or filename.endswith("unicode.py"):
            self.import_manager = None
            self.modules_analyzed = set()
            self.filename = None
            return
        super().__init__(filename, modname, modules_analyzed)
        self.modname = modname
        if self.current_ns:
            imp = self.get_module_ns(self.current_ns)
            self.modname = imp.name
            self.filename = imp.filename
        self.mod_dir = "/".join(self.filename.split("/")[:-1])
        self.import_manager: ImportManager = import_manager
        self.scope_manager: ScopeManager = scope_manager
        self.def_manager: DefinitionManager = def_manager
        self.class_manager: ClassManager = class_manager
        self.module_manager: ModuleManager = module_manager
        self.change_manager: ChangeManager = change_manager
        self.node_manager: NodeManager = node_manager
        self.match = {}
        self.decy = decy
        self.cg: CallGraph = cg
        self.callStack = callStack
        self.visited_scope = visited_scope
    def flatten(self, a):
        if not isinstance(a, (list,)):
            return [a]
        else:
            b = []
            for item in a:
                b += self.flatten(item)
        return b

    def getYPOint(self, row, yList):
        def closure():
            def func(callee):
                if isinstance(callee, Definition):
                    callee = callee.get_ns()
                if isinstance(callee, ScopeItem):
                    callee = callee.get_ns()
                return self.resolve(callee, row)

            return func

        if not isinstance(yList, list):
            yList = [yList]
        yList = self.flatten(yList)
        yList = list(filter(lambda x: x, yList))
        if not yList:
            return []
        return reduce(lambda x, y: x + y, map(closure(), yList))

    def pushStack(self, callDefi: Definition, isVisited=True, isEntry=False):
        if not callDefi:
            return
        callNs = callDefi.get_ns()
        if callNs in self.callStack:
            if gol.get_value('precision',False):
                self.cg.add_edge(self.current_ns, callNs)
            return
        gol.add_value('cnt')
        # # if gol.get_value('cnt') % 10 == 0:
        # with open(base + "text.txt",'a') as f:
        #     f.write("{}:{}\n".format(len(self.scope_manager.scopes),len(self.def_manager.defs)))

        if callDefi.get_type() == utils.constants.FUN_DEF:
            self.cg.add_edge(self.current_ns, callDefi.get_ns())
        if callDefi.get_type() == utils.constants.CLS_DEF:
            if not gol.get_value('precision', False):
                self.cg.add_edge(self.current_ns, callDefi.get_ns())
            pass
        if callDefi.get_type() == utils.constants.EXT_DEF:
            if not gol.get_value('precision', False):
                self.cg.add_edge(self.current_ns, callDefi.get_ns())
            pass
        if callDefi.get_type() == utils.constants.MOD_DEF:
            if not gol.get_value('precision', False):
                self.cg.add_edge(self.current_ns, callDefi.get_ns())
            pass
        curScope: ScopeItem = self.scope_manager.get_scope(self.current_ns)
        callScope: ScopeItem = self.scope_manager.get_scope(callNs)
        if isVisited:
            if (
                    callDefi.get_type() == utils.constants.FUN_DEF
                    and str(callScope) in self.visited_scope
            ):
                return
        self.callStack.append(callDefi.get_ns())
        gol.add_value(callDefi.get_ns())
        self.visited_scope.add(str(callScope))
        node = self.node_manager.get(callNs)
        if not node:
            self.callStack.pop()
            return
        imp = self.module_manager.get(self.get_module_ns(callNs))
        self.import_manager.set_current_mod(imp.name, imp.filename)
        method = None
        if callDefi.get_type() == utils.constants.ELSE_DEF:
            method = "visit_else"
        elif callDefi.get_type() == utils.constants.WHILE_DEF:
            method = "visit_With"
        else:
            method = "visit_" + node.__class__.__name__
        visitor = getattr(super(), method, self.generic_visit)
        if callDefi.get_type() == utils.constants.IF_DEF:
            visitor(node, utils.get_if_name(curScope.get_if_counter()))
        elif callDefi.get_type() == utils.constants.ELSE_DEF:
            visitor(node, utils.get_else_name(curScope.get_if_counter()))
        elif callDefi.get_type() == utils.constants.LAMBDA_NAME:
            visitor(node, utils.get_lambda_name(curScope.get_if_counter()))
        elif callDefi.get_type() == utils.constants.LIST_DEF:
            visitor(node, utils.get_list_name(curScope.get_list_counter()))
        elif callDefi.get_type() == utils.constants.MAP_DEF:
            visitor(node, utils.get_dict_name(curScope.get_dict_counter()))
        else:
            visitor(node)
        if isEntry:
            if hasattr(node, "lineno"):
                self.popStack(node.lineno, isEntry)
            else:
                self.popStack()
        else:
            self.popStack()
        pass

    def popStack(self, row=0, isEntry=False):
        callNs: str = self.callStack.pop()
        callDefi: Definition = self.def_manager.get(callNs)
        callScope: ScopeItem = self.scope_manager.get_scope(callNs)
        if callScope:
            callScope.reset_counters()

        def update_change(change: dict):
            for key, change in change.items():
                scopens = self.get_scope_ns(key)
                if not scopens:
                    return
                scope: ScopeItem = self.scope_manager.get_scope(scopens)
                if not scope:
                    return
                field = key[len(scopens) + 1:]
                defi: Definition = self.def_manager.get(key)
                if not defi:
                    defi = self.def_manager.create(key, utils.constants.NAME_DEF)
                defi.add_value_point(row, change.get_last_point_value())
                scope.add_def(field, defi)

        if isEntry:
            if self.change_manager.getChange(callNs):
                update_change(self.change_manager.getChange(callNs))
        if not self.current_ns:
            return
        imp = self.module_manager.get(self.get_module_ns(self.current_ns))
        self.import_manager.set_current_mod(imp.name, imp.filename)

    def visit_Module(self, node):
        def iterate_mod_items(items, const):
            for item in items:
                defi = self.def_manager.get(item)
                if not defi:
                    defi = self.def_manager.create(item, const)
                splitted = item.split(".")
                name = splitted[-1]
                parentns = ".".join(splitted[:-1])
                self.scope_manager.get_scope(parentns).add_def(name, defi)
                if const == utils.constants.CLS_DEF:
                    self.class_manager.create(item, self.modname)

        self.cg.add_node(self.modname, self.modname)
        self.import_manager.set_current_mod(self.modname, self.filename)
        mod = self.module_manager.create(self.modname, self.filename)
        first = 1
        last = len(self.contents.splitlines())
        if last == 0:
            first = 0
        mod.add_method(self.modname, first, last)
        root_sc = self.scope_manager.get_scope(self.modname)
        self.node_manager.add(self.modname, node)
        defi: Definition = self.def_manager.get(self.modname)
        if not defi:
            defi = self.def_manager.create(self.modname, utils.constants.MOD_DEF)
        else:
            defi.def_type = utils.constants.MOD_DEF
        self.node_manager.add(self.modname, node)
        if not root_sc or root_sc:
            # initialize module scopes
            items = self.scope_manager.handle_module(
                self.modname, self.filename, self.contents
            )
            root_sc = self.scope_manager.get_scope(self.modname)
            root_defi = self.def_manager.get(self.modname)
            if not root_defi:
                root_defi = self.def_manager.create(
                    self.modname, utils.constants.MOD_DEF
                )
            root_sc.add_def(self.modname.split(".")[-1], root_defi)
            # create function and class defs and add them to their scope
            # we do this here, because scope_manager doesn't have an
            # interface with def_manager, and we want function definitions
            # to have the correct points_to set
            iterate_mod_items(items["functions"], utils.constants.FUN_DEF)
            iterate_mod_items(items["classes"], utils.constants.CLS_DEF)
            self.pushStack(root_defi)
        self.modules_analyzed.add(self.filename)

    def visit_ImportFrom(self, node):
        self.visit_Import(node, prefix=node.module, level=node.level)

    def visit_With(self, node):
        current_scope: ScopeItem = self.scope_manager.get_scope(self.current_ns)
        if_counter = current_scope.inc_while_counter()
        if_name = utils.get_while_name(if_counter)
        if_full_ns = utils.join_ns(self.current_ns, if_name)
        # create a scope for the lambda
        self.scope_manager.create_scope(if_full_ns, current_scope)
        if_def = self.def_manager.handle_if_def(
            self.current_ns, if_name, utils.constants.WHILE_DEF
        )
        # add it to the current scope
        current_scope.add_def(if_name, if_def)
        for item in node.items:
            self.visit(item.context_expr)
            if not item.optional_vars:
                return
            self.visit(item.optional_vars)
            if isinstance(item.context_expr, ast.Call):
                leftDefi = self.decode_node(item.context_expr.func)
                self.visit_Call(item.context_expr)
            else:
                leftDefi = self.decode_node(item.context_expr)
            rightNs = self._get_target_ns(item.optional_vars)
            if rightNs:
                rightNs = rightNs[0]
            else:
                return
            rightDefi: Definition = self.def_manager.get(rightNs)
            if not rightDefi:
                rightDefi = self.def_manager.create(rightNs, utils.constants.NAME_DEF)
            if leftDefi:
                if not leftDefi[0]:
                    continue
                function1Ns = utils.join_ns(leftDefi[0].get_ns(), "__enter__")
                function2Ns = utils.join_ns(leftDefi[0].get_ns(), "__exit__")
                
                # function1Defi = self.def_manager.get(function1Ns)
                # function2Defi = self.def_manager.get(function2Ns)
                # function1Defi = self.getYPOint(node.lineno,[function1Ns])
                # function2Defi = self.getYPOint(node.lineno,[function2Ns])
                # tmp1 = self.find_field(leftDefi[0].get_ns(),"__enter__")
                # tmp2 = self.find_field(leftDefi[0].get_ns(),"__exit__")
                function1Defi = self.find_field(leftDefi[0].get_ns(),"__enter__")
                function2Defi = self.find_field(leftDefi[0].get_ns(),"__exit__")
                # print(tmp1.get_ns(),tmp2.get_ns())

                # print(function1Defi,function2Defi)
                # for d in function1Defi:
                #     self.pushStack(d, isEntry=True)
                # for d in function2Defi:
                #     self.pushStack(d, isEntry=True)
                self.pushStack(function1Defi, isEntry=True)
                self.pushStack(function2Defi, isEntry=True)
                leftPoint = self.getYPOint(
                    node.lineno, utils.join_ns(function1Ns, utils.constants.RETURN_NAME)
                )
                self.scope_manager.handle_assign(
                    self.current_ns, rightNs[len(self.current_ns) + 1:], rightDefi
                )
                rightDefi.add_value_point(node.lineno, leftPoint)
        self.node_manager.add(if_full_ns, node)
        self.pushStack(if_def)
        pass

    def visit_Import(self, node, prefix="", level=0):
        """
        For imports of the form
            `from something import anything`
        prefix is set to "something".
        For imports of the form
            `from .relative import anything`
        level is set to a number indicating the number
        of parent directories (e.g. in this case level=1)
        """

        def handle_src_name(name):
            # Get the module name and prepend prefix if necessary
            src_name = name
            if prefix:
                src_name = prefix + "." + src_name
            return src_name

        def handle_scopes(imp_name, tgt_name, modname):
            def create_def(scope, name):
                if name not in scope.get_defs():
                    def_ns = utils.join_ns(scope.get_ns(), name)
                    defi = self.def_manager.get(def_ns)
                    if not defi:
                        defi = self.def_manager.create(def_ns, utils.constants.NAME_DEF)
                    current_scope.add_def(name, defi)

            current_scope = self.scope_manager.get_scope(self.current_ns)
            imported_scope = self.scope_manager.get_scope(modname)
            if tgt_name == "*":
                if imported_scope:
                    for name, defi in imported_scope.get_defs().items():
                        create_def(current_scope, name)
                        current_scope.get_def(name).add_value_point(
                            node.lineno, defi.get_ns()
                        )
            else:
                if imported_scope:
                    defi = imported_scope.get_def(imp_name)
                    if not defi:
                        defi = self.def_manager.get(imp_name)
                    if not defi:
                        return
                    if (
                            modname == tgt_name
                            and defi.get_type() != utils.constants.MOD_DEF
                    ):
                        create_def(current_scope, tgt_name)
                        current_scope.get_def(tgt_name).add_value_point(
                            node.lineno, modname
                        )
                    else:
                        create_def(current_scope, tgt_name)
                        current_scope.get_def(tgt_name).add_value_point(
                            node.lineno, defi.get_ns()
                        )

        # 加入ext_def，会出现指向
        def add_external_def(name, target, row=0):
            # add an external def for the name
            defi = self.def_manager.get(name)
            if not defi:
                defi = self.def_manager.create(name, utils.constants.EXT_DEF)
            scope = self.scope_manager.get_scope(self.current_ns)
            if target != "*":
                # add a def for the target that points to the name
                tgt_ns = utils.join_ns(scope.get_ns(), target)
                tgt_defi: Definition = self.def_manager.get(tgt_ns)
                if not tgt_defi:
                    tgt_defi = self.def_manager.create(tgt_ns, utils.constants.NAME_DEF)
                # tgt_defi.add_name_point(row).add(defi.get_ns())
                tgt_defi.add_value_point(row, defi.get_ns())
                scope.add_def(target, tgt_defi)

        for import_item in node.names:
            src_name = handle_src_name(import_item.name)
            tgt_name = import_item.asname if import_item.asname else import_item.name
            if src_name == "tldextract":
                print()
            if tgt_name == "TLDExtract":
                print()
            imported_name = self.import_manager.handle_import(src_name, level)
            if not imported_name:
                add_external_def(src_name, tgt_name, node.lineno)
                continue
            fname = self.import_manager.get_filepath(imported_name)
            if not fname:
                add_external_def(src_name, tgt_name)
                continue
            if not self.decy:
                if self.import_manager.get_mod_dir() not in fname:
                    add_external_def(src_name, tgt_name)
                    continue
            if fname.endswith(".py") and not imported_name in self.modules_analyzed:
                self.analyze_submodule(imported_name)
            if not gol.get_value('precision', False):
                self.cg.add_edge(self.current_ns, imported_name)
            handle_scopes(import_item.name, tgt_name, imported_name)

    def visit_If(self, node):
        def process_if_main():
            nodeTest: ast.Compare = node.test
            if not isinstance(nodeTest, ast.Compare):
                return False
            if (
                    isinstance(nodeTest.left, ast.Name)
                    and nodeTest.left.id == "__name__"
                    and nodeTest.comparators
                    and isinstance(nodeTest.comparators[0], ast.Constant)
                    and nodeTest.comparators[0].value == "__main__"
            ):
                modNs = self.get_module_ns(self.current_ns)
                if modNs not in self.module_manager.local:
                    return True
            return False

        # The name of a lambda is defined by the counter of the current scope
        current_scope = self.scope_manager.get_scope(self.current_ns)
        if_counter = current_scope.inc_if_counter()
        if_name = utils.get_if_name(if_counter)
        if_full_ns = utils.join_ns(self.current_ns, if_name)
        # create a scope for the lambda
        self.scope_manager.create_scope(if_full_ns, current_scope)
        if_def = self.def_manager.handle_if_def(self.current_ns, if_name)
        # add it to the current scope
        current_scope.add_def(if_name, if_def)

        self.visit(node.test)
        if process_if_main():
            return
        self.node_manager.add(if_full_ns, node)
        # super().visit_If(node, if_name)
        # 如果有orelse，就说明有else
        if hasattr(node, "orelse") and len(node.orelse) > 0:
            current_scope = self.scope_manager.get_scope(self.current_ns)
            if_counter = current_scope.get_if_counter()
            else_name = utils.get_else_name(if_counter)
            else_full_ns = utils.join_ns(self.current_ns, else_name)
            self.scope_manager.create_scope(else_full_ns, current_scope)
            else_def = self.def_manager.handle_if_def(
                self.current_ns, else_name, utils.constants.ELSE_DEF
            )
            current_scope.add_def(else_name, else_def)
            self.match[if_full_ns] = else_full_ns
            self.node_manager.add(else_full_ns, node)
            self.pushStack(else_def)
        else:
            self.match[if_full_ns] = None
        self.pushStack(if_def)
        changeList = self.mergeIfElse(if_full_ns, self.match[if_full_ns], node.lineno)

        self.update(self._get_last_line(node), changeList)

    def visit_While(self, node):
        self.visit_If(node)
        pass

    def visit_Assign(self, node):
        self._visit_assign(node.value, node.targets, node.lineno)

    def _visit_assign(self, value, targets, row=0):
        # 先执行右边
        self.visit(value)
        decoded = self.decode_node(value)

        def assign(xList, y):
            for x in xList:
                x_defi = None
                if isinstance(x, str):
                    x_defi: Definition = self.get_or_create(
                        self.current_ns,
                        x[len(self.current_ns) + 1:],
                        utils.constants.NAME_DEF,
                    )
                elif isinstance(x, Definition):
                    x_defi = x
                if not x_defi:
                    return
                curNsDefi: Definition = self.def_manager.get(self.current_ns)
                try:
                    iter(decoded)
                except TypeError:
                    return
                if not y:
                    y_point = []
                else:
                    y_point = self.getYPOint(row, y)
                if curNsDefi.get_type() not in [
                    utils.constants.IF_DEF,
                    utils.constants.WHILE_DEF,
                    utils.constants.ELSE_DEF,
                ]:
                    x_defi.add_value_point(row, y_point)
                else:
                    if self.iSDefiInScope(x_defi.get_ns(), self.current_ns):
                        x_defi.add_value_point(row, y_point)
                    else:
                        self.change_manager.addChange(
                            self.current_ns, x_defi.get_ns(), row, y_point
                        )
            pass

        def store(xList, f, y):
            curScope: ScopeItem = self.scope_manager.get_scope(self.current_ns)
            xPointList = self.getYPOint(row, xList)
            y_point = self.getYPOint(row, y)
            for x in xPointList:
                if (
                        curScope.get_def(x)
                        and curScope.get_def(x).get_type() == utils.constants.NAME_DEF
                ):
                    curScope.get_def(x).add_value_point(row, y_point)
                else:
                    self.change_manager.addChange(
                        self.current_ns, utils.join_ns(x, f), row, y_point
                    )
                    defi: Definition = self.def_manager.get(utils.join_ns(x, f))
                    if defi:
                        defi.add_value_point(row, y_point)
            pass

        def do_assign(decoded, target):
            self.visit(target)
            try:
                iter(decoded)
            except TypeError:
                return
            # decoded = list(filter(lambda x: x is not None, decoded))
            if isinstance(target, ast.Tuple):
                for pos, elt in enumerate(target.elts):
                    if not isinstance(decoded, Definition) and pos < len(decoded):
                        do_assign(decoded[pos], elt)
            else:
                if isinstance(target, ast.Name):
                    curNsDefi: Definition = self.def_manager.get(self.current_ns)
                    if curNsDefi.get_type() not in [
                        utils.constants.IF_DEF,
                        utils.constants.WHILE_DEF,
                        utils.constants.ELSE_DEF,
                    ]:
                        assign(self._get_target_ns(target), decoded)
                    else:
                        leftTarget = self.scope_manager.get_def(
                            self.current_ns, target.id
                        )
                        if not leftTarget:
                            leftTargetNs = utils.join_ns(self.current_ns, target.id)
                            leftTargetDefi = self.def_manager.create(
                                leftTargetNs, utils.constants.NAME_DEF
                            )
                            self.scope_manager.handle_assign(
                                self.current_ns, target.id, leftTargetDefi
                            )
                        assign(self.decode_node(target), decoded)
                elif isinstance(target, ast.Attribute):
                    store(self.decode_node(target.value), target.attr, decoded)
                elif isinstance(target, ast.Subscript):
                    decoded = self.flatten(decoded)
                    decoded = list(filter(lambda x: x is not None, decoded))
                    # leftList = self.getYPOint(target.lineno,self._get_target_ns(target.value))
                    leftList = self.getYPOint(target.lineno, self.decode_node(target.value))

                    # left = self.getYPOint(row,self.decode_node(target.value))
                    for left in leftList:
                        leftDefi: Definition = self.def_manager.get(left)
                        if not leftDefi or leftDefi.get_type() not in [utils.constants.LIST_DEF,
                                                                       utils.constants.MAP_DEF]:
                            continue
                        if getattr(target.slice, "value", None) is not None and self._is_literal(target.slice.value):
                            sl_names = [target.slice.value]
                        else:
                            # sl_names = self.decode_node(target.slice)
                            sl_names = self.decode_node(target.value)
                        keys = set()
                        for s in sl_names:
                            if isinstance(s, Definition):
                                keys.add(s.get_ns())
                            elif isinstance(s, str):
                                keys.add(s)
                            elif isinstance(s, int):
                                keys.add(s)
                        for key in keys:
                            for x in decoded:
                                if not x:
                                    print()
                            leftDefi.set_element(key, list(map(lambda x: x.get_ns() if isinstance(x,Definition) else x, decoded)))

        for target in targets:
            do_assign(decoded, target)

    def visit_Lambda(self, node):
        # The name of a lambda is defined by the counter of the current scope
        fn_ns = self._handle_ns()
        current_scope = self.scope_manager.get_scope(self.current_ns)
        lambda_counter = current_scope.inc_lambda_counter()
        lambda_name = utils.get_lambda_name(lambda_counter)
        lambda_full_ns = utils.join_ns(self.current_ns, lambda_name)

        # create a scope for the lambda
        self.scope_manager.create_scope(lambda_full_ns, current_scope)
        lambda_def = self._handle_function_def(node, lambda_name, fn_ns)
        current_scope.add_def(lambda_name, lambda_def)
        self.node_manager.add(lambda_full_ns, node)


    def visit_List(self, node):
        list_counter = self.scope_manager.get_scope(self.current_ns).inc_list_counter()
        list_name = utils.get_list_name(list_counter)
        defiNs = utils.join_ns(self.current_ns, list_name)
        list_defi: Definition = self.def_manager.get(defiNs)
        if not list_defi:
            list_defi = self.def_manager.create(defiNs, utils.constants.LIST_DEF)
            self.scope_manager.handle_assign(self.current_ns, list_name, list_defi)
            self.node_manager.add(list_defi.get_ns(), node)
            current_scope: ScopeItem = self.scope_manager.get_scope(self.current_ns)
            self.scope_manager.create_scope(list_defi.get_ns(), current_scope)
        else:
            list_defi.def_type = utils.constants.LIST_DEF
        self.pushStack(list_defi)
        for idx, elt in enumerate(node.elts):
            # self.visit(elt)
            # tmp = self.decode_node(elt)
            # key_full_ns = utils.join_ns(list_defi.get_ns(), utils.get_int_name(idx))
            # key_def:Definition = self.def_manager.get(key_full_ns)
            # if not key_def:
            #     key_def = self.def_manager.create(key_full_ns, utils.constants.NAME_DEF)
            # idx += 1
            decoded_elt = self.decode_node(elt, utils.get_list_name(idx + 1))
            decoded_elt = self.getYPOint(node.lineno, decoded_elt)
            list_defi.set_element(idx, decoded_elt)
            # key_def.add_value_point(node.lineno,decoded_elt)
            # for v in decoded_elt:
            #     if isinstance(v, Definition):
            #         key_def.add_value_point(node.lineno,[v.get_ns()])
            #     else:
            #         key_def.get_lit_pointer().add(v)
        pass

    def visit_Dict(self, node):
        dict_counter = self.scope_manager.get_scope(self.current_ns).inc_dict_counter()
        dict_name = utils.get_dict_name(dict_counter)
        defiNs = utils.join_ns(self.current_ns, dict_name)
        dict_defi: Definition = self.def_manager.get(defiNs)
        if not dict_defi:
            dict_defi = self.def_manager.create(defiNs, utils.constants.MAP_DEF)
            self.scope_manager.handle_assign(self.current_ns, dict_name, dict_defi)
            self.node_manager.add(dict_defi.get_ns(), node)
            current_scope: ScopeItem = self.scope_manager.get_scope(self.current_ns)
            self.scope_manager.create_scope(dict_defi.get_ns(), current_scope)
        self.pushStack(dict_defi)
        for key, val in zip(node.keys, node.values):
            # self.visit(elt)
            # tmp = self.decode_node(elt)
            # key_full_ns = utils.join_ns(list_defi.get_ns(), utils.get_int_name(idx))
            # key_def:Definition = self.def_manager.get(key_full_ns)
            # if not key_def:
            #     key_def = self.def_manager.create(key_full_ns, utils.constants.NAME_DEF)
            decoded_elt = self.decode_node(val, utils.get_dict_name(
                self.scope_manager.get_scope(self.current_ns).get_dict_counter()))
            decoded_elt = self.getYPOint(node.lineno, decoded_elt)
            dict_defi.set_element(key, decoded_elt)
            # key_def.add_value_point(node.lineno,decoded_elt)
            # for v in decoded_elt:
            #     if isinstance(v, Definition):
            #         key_def.add_value_point(node.lineno,[v.get_ns()])
            #     else:
            #         key_def.get_lit_pointer().add(v)
        pass
        pass
    def _get_fun_defaults(self, node):
        defaults = {}
        if node.args.posonlyargs:
            start = len(node.args.args) - len(node.args.defaults)
            for cnt, d in enumerate(node.args.defaults, start=start):
                if not d:
                    continue
                self.visit(d)
                # defaults[node.args.args[cnt].arg] = self.decode_node(d)
                # print(node.lineno)
                # print(cnt,node.args.posonlyargs)
                if cnt >= len(node.args.posonlyargs):
                    continue
                defaults[node.args.posonlyargs[cnt].arg] = self.getYPOint(
                    node.lineno, self.decode_node(d)
                )
            return defaults
        # try:
        start = len(node.args.args) - len(node.args.defaults)

        for cnt, d in enumerate(node.args.defaults, start=start):
            if not d:
                continue
            self.visit(d)
            defaults[node.args.args[cnt].arg] = self.getYPOint(
                node.lineno, self.decode_node(d)
            )
        return defaults

    def _handle_function_def(self, node, fn_name, fn_ns):
        currentNsDefi = self.def_manager.get(fn_ns)
        defaults = self._get_fun_defaults(node)
        fn_def: Definition = self.def_manager.handle_function_def(fn_ns, fn_name)
        fn_scope: ScopeItem = self.scope_manager.get_scope(fn_def.get_ns())
        if not fn_scope:
            fn_scope = self.scope_manager.create_scope(
                fn_def.get_ns(), self.scope_manager.get_scope(fn_ns)
            )
        ret_def: Definition = self.def_manager.get(
            utils.join_ns(fn_def.get_ns(), utils.constants.RETURN_NAME)
        )
        fn_scope.add_def(utils.constants.RETURN_NAME, ret_def)
        modNs = self.get_module_ns(self.current_ns)
        mod = self.module_manager.get(modNs)
        if not mod:
            mod = self.module_manager.create(self.modname, self.filename)
        mod.add_method(fn_def.get_ns(), node.lineno, self._get_last_line(node))
        defs_to_create = []

        is_static_method = False
        tmpargs = node.args.args[:]
        if hasattr(node, "decorator_list"):
            for decorator in node.decorator_list:
                if (
                        isinstance(decorator, ast.Name)
                        and decorator.id == utils.constants.STATIC_METHOD
                ):
                    is_static_method = True
        if (
                currentNsDefi.get_type() == utils.constants.CLS_DEF
                and not is_static_method
                and node.args.args
        ):
            arg_ns = utils.join_ns(fn_def.get_ns(), node.args.args[0].arg)
            arg_def = self.def_manager.get(arg_ns)
            if not arg_def:
                arg_def = self.def_manager.create(arg_ns, utils.constants.PARAM_DEF)
            arg_def.add_value_point(
                node.lineno, utils.join_ns(currentNsDefi.get_ns(), "self")
            )
            self.scope_manager.handle_assign(
                fn_def.get_ns(), node.args.args[0].arg, arg_def
            )
            tmpargs = node.args.args[1:]

        for pos, arg in enumerate(tmpargs):
            arg_ns = utils.join_ns(fn_def.get_ns(), arg.arg)
            defs_to_create.append(arg_ns)

        for arg in node.args.kwonlyargs:
            arg_ns = utils.join_ns(fn_def.get_ns(), arg.arg)
            defs_to_create.append(arg_ns)
        for arg_ns in defs_to_create:
            arg_def = self.def_manager.get(arg_ns)
            if not arg_def:
                arg_def: Definition = self.def_manager.create(
                    arg_ns, utils.constants.PARAM_DEF
                )
            self.scope_manager.handle_assign(
                fn_def.get_ns(), arg_def.get_name(), arg_def
            )
            arg_name = arg_ns.split(".")[-1]
            if defaults.get(arg_name, None):
                arg_def.add_value_point(node.lineno, defaults[arg_name])
            self.scope_manager.add_params(fn_def.get_ns(), arg_def)
        return fn_def

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_For(self, node):
        self.visit(node.iter)
        self.visit(node.target)
        # if isinstance(node.iter,tuple):
        if isinstance(node.target,ast.Name):
            tmpList = self._get_target_ns(node.target)
            for tmp in tmpList:
                if not self.def_manager.get(tmp):
                    tmpDefi = self.def_manager.create(tmp,utils.constants.NAME_DEF)
                    self.scope_manager.handle_assign(self.current_ns, node.target.id, tmpDefi)
        elif isinstance(node.target,tuple):
            for x in node.target.elts:
                if isinstance(x, ast.Name):
                    tmpList = self._get_target_ns(x)
                    for tmp in tmpList:
                        if not self.def_manager.get(tmp):
                            tmpDefi = self.def_manager.create(tmp, utils.constants.NAME_DEF)
                            self.scope_manager.handle_assign(self.current_ns, x.target.id, tmpDefi)
        pointList = []
        inodeList = self.decode_node(node.target)
        if isinstance(node.iter,ast.Call):
            iter_decoded = self.decode_node(node.iter.func)
        elif isinstance(node.iter,ast.Name):
            iter_decoded = self.decode_node(node.iter)
        else:
            iter_decoded = []
        for item in iter_decoded:
            if not isinstance(item, Definition):
                continue
            names = self.getYPOint(node.lineno, item.get_ns())
            for name in names:
                iter_ns = utils.join_ns(name, utils.constants.ITER_METHOD)
                next_ns = utils.join_ns(name, utils.constants.NEXT_METHOD)
                return_ns = utils.join_ns(name, utils.constants.RETURN_NAME)
                iter_return_ns = utils.join_ns(name, utils.constants.ITER_METHOD,utils.constants.RETURN_NAME)
                next_return_ns = utils.join_ns(name, utils.constants.NEXT_METHOD,utils.constants.RETURN_NAME)
                if self.def_manager.get(iter_ns):
                    # self.cg.add_edge(self.current_ns, iter_ns)
                    self.pushStack(self.def_manager.get(iter_ns))
                if self.def_manager.get(next_ns):
                    # self.cg.add_edge(self.current_ns, next_ns)
                    self.pushStack(self.def_manager.get(next_ns))
                if self.def_manager.get(iter_return_ns):
                    pointList += self.getYPOint(node.lineno, iter_return_ns)
                if self.def_manager.get(next_return_ns):
                    pointList += self.getYPOint(node.lineno, next_return_ns)
                if self.def_manager.get(return_ns):
                    pointList += self.getYPOint(node.lineno, return_ns)
        pointList = list(set(pointList))
        for inode in inodeList:
            if isinstance(inode,Definition):
                inode.add_value_point(node.lineno,pointList)
        super().visit_For(node)

    def visit_FunctionDef(self, node):
        curNs = self._handle_ns()
        fn_def = self._handle_function_def(node, node.name, curNs)
        curScope: ScopeItem = self.scope_manager.get_scope(curNs)
        fn_scope: ScopeItem = self.scope_manager.get_scope(fn_def.get_ns())
        if not self.scope_manager.get_scope(fn_def.get_ns()):
            fn_scope = self.scope_manager.create_scope(fn_def.get_ns(), curScope)
        curScope.add_def(node.name, fn_def)
        self.node_manager.add(fn_def.get_ns(), node)

        if node.decorator_list:
            reversed_decorators = list(reversed(node.decorator_list))
            if hasattr(fn_def, "decorator_names") and reversed_decorators:
                last_decoded = self.decode_node(reversed_decorators[-1])
                for d in last_decoded:
                    if not isinstance(d, Definition):
                        continue
            for index, decorator in enumerate(reversed_decorators):
                if index == 0:
                    self.visit_Call(decorator, True, [fn_def])
                else:
                    decorate_defi_list = self.getYPOint(node.lineno, self.decode_node(reversed_decorators[index - 1]))
                    decorate_return_list = list(
                        map(lambda x: utils.join_ns(x, utils.constants.RETURN_NAME), decorate_defi_list))
                    # self.visit_Call(decorator, True, self.decode_node(reversed_decorators[index-1]))
                    self.visit_Call(decorator, True, decorate_return_list)
        # self.pushStack(fn_def)
        # super().visit_FunctionDef(node)
        pass

    def _get_last_line(self, node):
        lines = sorted(
            list(ast.walk(node)),
            key=lambda x: x.lineno if hasattr(x, "lineno") else 0,
            reverse=True,
        )
        if not lines:
            return node.lineno
        last = getattr(lines[0], "lineno", node.lineno)
        if last < node.lineno:
            return node.lineno
        return last

    def visit_ClassDef(self, node):
        cls_ns = self._handle_ns()
        cls_def: Definition = self.def_manager.handle_class_def(
            self.current_ns, node.name, cls_ns
        )
        cls_scope: ScopeItem = self.scope_manager.get_scope(cls_def.get_ns())
        if not self.scope_manager.get_scope(cls_def.get_ns()):
            cls_scope = self.scope_manager.create_scope(
                cls_def.get_ns(), self.scope_manager.get_scope(cls_ns)
            )
        cls: ClassNode = self.class_manager.get(cls_def.get_ns())
        if not cls:
            cls: ClassNode = self.class_manager.create(cls_def.get_ns(), self.modname)
        cls_ret = utils.join_ns(cls_def.get_ns(), utils.constants.RETURN_NAME)
        cls_ret_defi: Definition = self.def_manager.get(cls_ret)
        cls_self = utils.join_ns(cls_def.get_ns(), "self")
        cls_self_defi: Definition = self.def_manager.get(cls_self)
        if not cls_ret_defi:
            cls_ret_defi = self.def_manager.create(cls_ret, utils.constants.RETURN_DEF)
        cls_scope.add_def(utils.constants.RETURN_NAME, cls_ret_defi)
        if not cls_self_defi:
            cls_self_defi = self.def_manager.create(cls_self, utils.constants.NAME_DEF)
        cls_scope.add_def("self", cls_self_defi)
        cls_ret_defi.add_value_point(node.lineno, [cls_def.get_ns()])
        cls_self_defi.add_value_point(node.lineno, [cls_def.get_ns()])

        curScope: ScopeItem = cls_scope.parent
        if not curScope:
            return
        curScope.add_def(node.name, cls_def)
        cls.clear_mro()
        for base in node.bases:
            # all bases are of the type ast.Name
            self.visit(base)
            # bases = self.decode_node(base)
            bases = self.getYPOint(node.lineno, self.decode_node(base))
            for base in bases:
                base_def: Definition = self.def_manager.get(base)
                if not isinstance(base_def, Definition):
                    continue
                names = set()
                if base_def.points:
                    names = base_def.get_last_point_value()
                else:
                    names.add(base_def.get_ns())
                for name in names:
                    # add the base as a parent
                    cls.add_parent(name)
                    # add the base's parents
                    parent_cls = self.class_manager.get(name)
                    # if parent_cls:
                    #     cls.add_parent(parent_cls.get_mro())
        mroList = cls.mro
        for name in mroList:
            parent_cls = self.class_manager.get(name)
            if parent_cls:
                cls.add_parent(parent_cls.get_mro())
        cls.compute_mro()
        self.node_manager.add(cls_def.get_ns(), node)
        self.pushStack(cls_def)
        pass

    def decode_node(self, node,index=None):
        if isinstance(node, ast.Name):
            return [self.scope_manager.get_def(self.current_ns, node.id)]
        elif isinstance(node, ast.Call):
            decoded = self.decode_node(node.func)
            return_defs = []
            for call_def in decoded:
                if not isinstance(call_def, Definition):
                    continue
                calleeNs = utils.join_ns(call_def.get_ns(), utils.constants.RETURN_NAME)
                defi = self.def_manager.get(calleeNs)
                if not defi:
                    defi = self.def_manager.create(calleeNs, utils.constants.NA_DEF)
                return_defs.append(defi)
            return return_defs
        elif isinstance(node, ast.Lambda):
            lambda_counter = self.scope_manager.get_scope(
                self.current_ns
            ).get_lambda_counter()
            lambda_name = utils.get_lambda_name(lambda_counter)
            return [self.scope_manager.get_def(self.current_ns, lambda_name)]
        elif isinstance(node, ast.Tuple):
            decoded = []
            for elt in node.elts:
                decoded.append(self.decode_node(elt))
            return decoded
        elif isinstance(node, ast.BinOp):
            decoded_left = self.decode_node(node.left)
            decoded_right = self.decode_node(node.right)
            if not isinstance(decoded_left, Definition):
                return decoded_left
            if not isinstance(decoded_right, Definition):
                return decoded_right
        elif isinstance(node, ast.Attribute):
            names = self.decode_node(node.value)
            defis = []
            for name in names:
                if not isinstance(name, Definition):
                    return defis
                ns = utils.join_ns(name.get_ns(), node.attr)
                defi = self.def_manager.get(ns)
                if defi:
                    defis.append(defi)
                else:
                    defi = self.def_manager.create(ns, utils.constants.NA_DEF)
                    defis.append(defi)
            return defis
        elif isinstance(node, ast.Num):
            # defiNs = utils.join_ns(self.current_ns, '<int>')
            defiNs = "<int>"
            defi = self.def_manager.get(defiNs)
            if not defi:
                defi = self.def_manager.create(defiNs, utils.constants.INT_DEF)
            return [defi]
        elif isinstance(node, ast.Str):
            defiNs = "<str>"
            defi = self.def_manager.get(defiNs)
            if not defi:
                defi = self.def_manager.create(defiNs, utils.constants.STR_DEF)
            return [defi]
        elif self._is_literal(node):
            return [node]
        # elif isinstance(node, ast.Dict):
        #     if not self.scope_manager.get_scope(self.current_ns):
        #         return ["dict"]
        #     dict_counter = self.scope_manager.get_scope(
        #         self.current_ns
        #     ).get_dict_counter()
        #     dict_name = utils.get_dict_name(dict_counter)
        #     defiNs = utils.join_ns(self.current_ns, dict_name)
        #     defi = self.def_manager.get(defiNs)
        #     if not defi:
        #         defi = self.def_manager.create(defiNs, utils.constants.MAP_DEF)
        #         self.scope_manager.handle_assign(self.current_ns, dict_name, defi)
        #     scope_def = self.scope_manager.get_def(self.current_ns, dict_name)
        #     return [self.scope_manager.get_def(self.current_ns, dict_name)]
        # elif isinstance(node, ast.List):
        #     list_counter = self.scope_manager.get_scope(
        #         self.current_ns
        #     ).get_list_counter()
        #     list_name = utils.get_list_name(list_counter)
        #     defiNs = utils.join_ns(self.current_ns, list_name)
        #     defi = self.def_manager.get(defiNs)
        #     if not defi:
        #         defi = self.def_manager.create(defiNs, utils.constants.LIST_DEF)
        #         self.scope_manager.handle_assign(self.current_ns, list_name, defi)
        #     return [self.scope_manager.get_def(self.current_ns, list_name)]
        elif isinstance(node, ast.Dict):
            if not index:
                if not self.scope_manager.get_scope(self.current_ns):
                    return ['dict']
                dict_counter = self.scope_manager.get_scope(self.current_ns).get_dict_counter()
                dict_name = utils.get_dict_name(dict_counter)
                defiNs = utils.join_ns(self.current_ns, dict_name)
                defi = self.def_manager.get(defiNs)
                if not defi:
                    defi = self.def_manager.create(defiNs, utils.constants.MAP_DEF)
                    self.scope_manager.handle_assign(self.current_ns, dict_name, defi)
                return [self.scope_manager.get_def(self.current_ns, dict_name)]
            else:
                curScope: ScopeItem = self.scope_manager.get_scope(utils.join_ns(self.current_ns))
                if not curScope:
                    return []
                dict_counter = curScope.get_dict_counter()
                dict_name = utils.get_dict_name(dict_counter)
                defiNs = utils.join_ns(self.current_ns, dict_name, index)
                defi = self.def_manager.get(defiNs)
                if not defi:
                    return "<dict>"
                # if not defi:
                #     defi = self.def_manager.create(defiNs, utils.constants.LIST_DEF)
                #     self.scope_manager.handle_assign(self.current_ns, list_name, defi)
                return [defiNs]
        elif isinstance(node, ast.List):
            if not index:
                if not self.scope_manager.get_scope(self.current_ns):
                    return ['list']
                list_counter = self.scope_manager.get_scope(self.current_ns).get_list_counter()
                list_name = utils.get_list_name(list_counter)
                defiNs = utils.join_ns(self.current_ns, list_name)
                defi = self.def_manager.get(defiNs)
                if not defi:
                    defi = self.def_manager.create(defiNs, utils.constants.MAP_DEF)
                    self.scope_manager.handle_assign(self.current_ns, list_name, defi)
                return [self.scope_manager.get_def(self.current_ns, list_name)]
            else:
                curScope: ScopeItem = self.scope_manager.get_scope(utils.join_ns(self.current_ns))
                if not curScope:
                    return []
                list_counter = curScope.get_dict_counter()
                list_name = utils.get_dict_name(list_counter)
                defiNs = utils.join_ns(self.current_ns, list_name, index)
                defi = self.def_manager.get(defiNs)
                if not defi:
                    return "<list>"
                # if not defi:
                #     defi = self.def_manager.create(defiNs, utils.constants.LIST_DEF)
                #     self.scope_manager.handle_assign(self.current_ns, list_name, defi)
                return [defiNs]
        elif isinstance(node, ast.Subscript):
            names = self.retrieve_subscript_names(node)
            defis = []
            for name in names:
                defi = self.def_manager.get(name)
                if defi:
                    defis.append(defi)
            return defis


        elif isinstance(node, ast.JoinedStr):
            return ["<str>"]
        return []

    def visit_Call(self, node, decorator=False, decoratorParam=None):
        def resolve_call():
            if decorator:
                if isinstance(node, ast.Name):
                    self.visit(node)
                    if getattr(node, "id", None) and self.is_builtin(node.id):
                        name = utils.join_ns(utils.constants.BUILTIN_NAME, node.id)
                        defi = self.def_manager.get(name)
                        if not defi:
                            self.def_manager.create(name, utils.constants.FUN_DEF)
                        return [name]
                    else:
                        curDefi: Definition = self.scope_manager.get_def(
                            self.current_ns, node.id
                        )
                        if not curDefi:
                            return []
                        # callDefiNsList = self.getPoint(curDefi.get_ns())
                        callDefiNsList = self.getYPOint(1000, [curDefi.get_ns()])
                        return callDefiNsList
                    pass
                elif isinstance(node, ast.Attribute):
                    self.visit(node)
                    field = node.attr
                    xDefiList = self.decode_node(node.value)
                    XPointList = (
                        self.getYPOint(node.lineno, xDefiList) if xDefiList else []
                    )
                    xFieldList = list(
                        filter(
                            lambda x: x,
                            (map(lambda x: self.find_field(x, field), XPointList)),
                        )
                    )
                    return self.getYPOint(node.lineno, xFieldList)
                    pass
                elif isinstance(node, ast.Call):
                    self.visit(node)
                    xDefiList = self.decode_node(node)
                    xRetList = self.getYPOint(node.lineno, xDefiList)
                    return xRetList
                elif isinstance(node, ast.Subscript):
                    # Calls can be performed only on single indices, not ranges
                    full_names = self.retrieve_subscript_names(node)
                    return [full_names]
                return
            if isinstance(node.func, ast.Name):
                self.visit(node.func)
                if getattr(node.func, "id", None) and self.is_builtin(node.func.id):
                    name = utils.join_ns(utils.constants.BUILTIN_NAME, node.func.id)
                    defi = self.def_manager.get(name)
                    if not defi:
                        self.def_manager.create(name, utils.constants.FUN_DEF)
                    return [name]
                else:
                    curDefi: Definition = self.scope_manager.get_def(
                        self.current_ns, node.func.id
                    )
                    if not curDefi:
                        return []
                    # callDefiNsList = self.getPoint(curDefi.get_ns())
                    callDefiNsList = self.getYPOint(1000, [curDefi.get_ns()])
                    return callDefiNsList
                pass
            elif isinstance(node.func, ast.Attribute):
                self.visit(node.func)
                field = node.func.attr
                xDefiList = self.decode_node(node.func.value)
                XPointList = self.getYPOint(node.lineno, xDefiList) if xDefiList else []
                xFieldList = list(
                    filter(
                        lambda x: x,
                        (map(lambda x: self.find_field(x, field), XPointList)),
                    )
                )
                for XPoint in XPointList:
                    Xdefi = self.def_manager.get(XPoint)
                    if isinstance(Xdefi,Definition) and Xdefi.get_type() == utils.constants.MAP_DEF:
                        if field in ['update']:
                            for index, param in enumerate(node.args):
                                if isinstance(param,ast.Dict):
                                    for index,v in enumerate(param.values):
                                        decoded = self.decode_node(v)
                                        values = self.getYPOint(node.lineno,decoded)
                                    # for v in param.values:
                                    #     values = self.getYPOint(node.lineno,v)
                                        Xdefi.set_element(index,values)
                            # XPoint.add_value_point()
                return self.getYPOint(node.lineno, xFieldList)
                pass
            elif isinstance(node.func, ast.Call):
                self.visit(node.func)
                xDefiList = self.decode_node(node.func)
                xRetList = self.getYPOint(node.lineno, xDefiList)
                return xRetList
            elif isinstance(node.func, ast.Subscript):
                # Calls can be performed only on single indices, not ranges
                full_names = self.retrieve_subscript_names(node.func)
                # return [full_names]
                return full_names
            return [None]

        def format_call(call):
            callDefi: Definition = self.def_manager.get(call)
            if callDefi and callDefi.get_type() == utils.constants.CLS_DEF:
                # clsCopyNs = self.new(call,node.lineno)
                clsInit = utils.join_ns(call, utils.constants.CLS_INIT)
                clsDefi = self.def_manager.get(clsInit)
                if clsDefi:
                    return clsInit
                else:
                    return None
            # if callDefi and callDefi.get_type() == utils.constants.FUN_DEF:
            #     return call
            return call

        def match_call(call):
            if decorator:
                callDefi: Definition = self.def_manager.get(call)
                if not callDefi:
                    # self.cg.add_edge(self.current_ns, call)
                    return
                callScope: ScopeItem = self.scope_manager.get_scope(call)
                if not callScope:
                    return
                moduleNs = self.get_module_ns(callScope.get_ns())
                method = self.module_manager.get_func_name(moduleNs, callScope.get_ns())
                if not method:
                    line = node.lineno
                else:
                    line = method["first"]
                paramList = callScope.params
                argList = decoratorParam
                paramsMap = {}
                for index, param in enumerate(decoratorParam):
                    if index >= len(argList):
                        break
                    if index >= len(paramList):
                        break
                    if isinstance(param, str) or isinstance(param, list):
                        paramsMap[paramList[index].get_ns()] = param
                    elif isinstance(param, Definition):
                        paramsMap[paramList[index].get_ns()] = param.get_ns()
                    elif isinstance(param, dict):
                        for k, v in param.items():
                            if not k:
                                continue
                            paramsMap[utils.join_ns(callScope.get_ns(), k)] = v
                for param, arg in paramsMap.items():
                    paramDefi: Definition = self.def_manager.get(param)
                    if (
                            not paramDefi
                            or not paramDefi.get_type() == utils.constants.PARAM_DEF
                    ):
                        continue
                    if isinstance(arg, str):
                        argsPoint = self.getYPOint(node.lineno, [arg])
                    elif isinstance(arg, list) and arg:
                        # argsPoint = reduce(lambda x, y: x + y, map(lambda x: self.getPoint(x), arg))
                        argsPoint = self.getYPOint(node.lineno, [arg])
                    elif isinstance(arg, ScopeItem):
                        # argsPoint = self.getPoint(arg.get_ns())
                        argsPoint = self.getYPOint(node.lineno, [arg])
                    paramDefi.add_value_point(line, argsPoint)

                return
            callDefi: Definition = self.def_manager.get(call)
            if not callDefi:
                # self.cg.add_edge(self.current_ns,call)
                return
            callScope: ScopeItem = self.scope_manager.get_scope(call)
            argList = self._handle_args(node)
            if not callScope:
                return
            moduleNs = self.get_module_ns(callScope.get_ns())
            method = self.module_manager.get_func_name(moduleNs, callScope.get_ns())
            if not method:
                line = node.lineno
            else:
                line = method["first"]
            paramList = callScope.params
            paramsMap = {}
            for index, param in enumerate(argList):
                if index >= len(argList):
                    break
                if isinstance(param, str) or isinstance(param, list):
                    if index >= len(paramList):
                        break
                    paramsMap[paramList[index].get_ns()] = param
                elif isinstance(param, ScopeItem):
                    paramsMap[paramList[index].get_ns()] = param
                elif isinstance(param, dict):
                    for k, v in param.items():
                        if not k:
                            continue
                        paramsMap[utils.join_ns(callScope.get_ns(), k)] = v
            for param, arg in paramsMap.items():
                paramDefi: Definition = self.def_manager.get(param)
                if (
                        not paramDefi
                        or not paramDefi.get_type() == utils.constants.PARAM_DEF
                ):
                    continue
                if isinstance(arg, str):
                    # argsPoint = self.getYPOint(node.lineno, [arg])
                    # argsPoint = self.getPoint(arg)
                    argsPoint = self.getYPOint(node.lineno, [arg])
                elif isinstance(arg, list) and arg:
                    # argsPoint = reduce(lambda x, y: x + y, map(lambda x: self.getPoint(x), arg))
                    argsPoint = self.getYPOint(node.lineno, arg)
                elif isinstance(arg, ScopeItem):
                    # argsPoint = self.getPoint(arg.get_ns())
                    argsPoint = self.getYPOint(node.lineno, [arg])
                else:
                    continue
                paramDefi.add_value_point(line, argsPoint)

        def enter_call(call: str):
            # self.cg.add_edge(self.current_ns, call)
            callDefi: Definition = self.def_manager.get(call)
            if callDefi and callDefi.get_type() != utils.constants.EXT_DEF:
                self.cg.add_edge(self.current_ns, call)
            tmp = reduce(
                lambda x, y: x or y, map(lambda x: x in call, utils.constants.BUILTTYPE)
            )
            if not callDefi and tmp:
                self.cg.add_edge(self.current_ns, call)
            self.pushStack(callDefi)
            pass

        def merge_change(callList):
            outPoint = {}
            for call in callList:
                callChange: dict = self.change_manager.getChange(call)
                if not callChange:
                    continue
                for key, point in callChange.items():
                    if key in outPoint:
                        outPoint[key] = outPoint[key].union(
                            point.get_last_point_value()
                        )
                    if key not in outPoint:
                        outPoint[key] = point.get_last_point_value()
            out = {}
            for key, point in outPoint.items():
                out[key] = ChangeItem(node.lineno, point)
            return out

        def update_change(change: dict):
            for key, change in change.items():
                scopens = self.get_scope_ns(key)
                if not scopens:
                    return
                scope: ScopeItem = self.scope_manager.get_scope(scopens)
                if not scope:
                    return
                field = key[len(scopens) + 1:]
                defi: Definition = self.def_manager.get(key)
                if not defi:
                    defi = self.def_manager.create(key, utils.constants.NAME_DEF)
                defi.add_value_point(node.lineno, change.get_last_point_value())
                scope.add_def(field, defi)
            pass
        # def builtin_function(func):
        #     if func == "<map>.update":

        # if hasattr(node, "func"):
        #     self.visit(node.func)
        callList = resolve_call()
        callList = filter(lambda x: x, callList)
        callList = list(filter(lambda x: x, map(format_call, callList)))
        # list(map(match_call, callList))
        list(map(match_call, callList))
        list(map(enter_call, callList))
        if not callList:
            if hasattr(node, "args"):
                self._handle_args(node)

        changeDict = merge_change(callList)
        for key, change in changeDict.items():
            self.change_manager.addChange(
                self.current_ns, key, node.lineno, change.get_last_point_value()
            )
        update_change(changeDict)

    def _handle_args(self, node):
        params_list = []

        for args_node in node.args:
            self.visit(args_node)
            decoded = self.decode_node(args_node)
            for args_defi in decoded:
                if isinstance(args_defi, Definition):
                    params_list.append(args_defi.get_ns())
                else:
                    params_list.append(args_defi)
        for keyword in node.keywords:
            tmpItem = {}
            self.visit(keyword.value)
            decoded = self.decode_node(keyword.value)
            paramDefiDict = {}
            for args_defi in decoded:
                if isinstance(args_defi, Definition):
                    if keyword not in paramDefiDict:
                        tmpItem.setdefault(keyword.arg, [args_defi.get_ns()])
                    else:
                        tmpItem[keyword].append(args_defi.get_ns())
                else:
                    if keyword not in paramDefiDict:
                        tmpItem.setdefault(keyword.arg, [args_defi])
                    else:
                        tmpItem[keyword.arg].append(args_defi)
            params_list.append(tmpItem)
        return params_list

    def visit_Return(self, node):
        self._visit_return(node)

    def visit_Yield(self, node):
        self._visit_return(node)

    def visit_Raise(self, node):
        if not node.exc:
            return
        self.visit(node.exc)
        decoded = self.decode_node(node.exc)
        for d in decoded:
            if not isinstance(d, Definition):
                continue
            names = self.getYPOint(node.lineno, d.get_ns())
            for name in names:
                pointer_def = self.def_manager.get(name)
                if not pointer_def:
                    continue
                if pointer_def.get_type() == utils.constants.CLS_DEF:
                    init_defi = self.find_cls_fun_ns(name, utils.constants.CLS_INIT)
                    if init_defi:
                        self.pushStack(init_defi)
                if pointer_def.get_type() == utils.constants.EXT_DEF:
                    self.cg.add_edge(self.current_ns, name)

    def _visit_return(self, node):
        if not node or not node.value:
            return
        self.visit(node.value)
        return_ns = utils.join_ns(self.current_ns, utils.constants.RETURN_NAME)
        self._handle_assign(
            return_ns,
            self.getYPOint(node.lineno, self.decode_node(node.value)),
            row=node.lineno,
            defiType=utils.constants.RETURN_DEF,
        )
        splitted = return_ns.split(".")
        self.scope_manager.handle_assign(
            ".".join(splitted[:-1]), splitted[-1], self.def_manager.get(return_ns)
        )

    def get_modules_analyzed(self):
        return self.modules_analyzed

    def analyze_submodules(self):
        super().analyze_submodules(
            ExtProcessor,
            self.import_manager,
            self.scope_manager,
            self.def_manager,
            self.class_manager,
            self.module_manager,
            self.call_manager,
            self.return_manager,
            self.cg,
            self.callStack,
            self.visited_scope,
            modules_analyzed=self.get_modules_analyzed(),
        )

    def analyze_submodule(self, imp):
        super().analyze_submodule(
            ExtProcessor,
            imp,
            self.import_manager,
            self.scope_manager,
            self.def_manager,
            self.class_manager,
            self.module_manager,
            self.change_manager,
            self.node_manager,
            self.cg,
            self.callStack,
            self.visited_scope,
            modules_analyzed=self.get_modules_analyzed(),
            decy=self.decy,
        )

    def visit_Try(self, node):
        for item in node.body:
            self.visit(item)
        for handler in node.handlers:
            self.visit(handler)
        pass

    def visit_ExceptHandler(self, node):
        for item in node.body:
            self.visit(item)
        pass

    def analyze(self):
        if not self.filename:
            return
        if not self.import_manager.get_node(self.modname):
            self.import_manager.create_node(self.modname)
            self.import_manager.set_filepath(self.modname, self.filename)

        try:
            self.visit(ast.parse(self.contents, self.filename))
        except Exception:
            pass
        # self.visit(ast.parse(self.contents, self.filename))

    def analyze_localfunction(self, localList):
        for local in localList:
            localDefi:Definition = self.def_manager.get(local)
            self.pushStack(localDefi, False, True)

    def analyze_allfunction(self):
        def analyze_local(local):
            moduleNode: Module = self.module_manager.get(local)
            if not moduleNode:
                return
            methodDict: dict = moduleNode.get_methods()
            for method in list(methodDict.keys()):
                methodDefi = self.def_manager.get(method)
                self.pushStack(methodDefi, False, True)

        prev = None

        def equal(prev):
            if not prev:
                return False
            if set(prev.keys()) == set(
                    self.module_manager.get_internal_modules().copy()
            ):
                return True
            return False

        cnt = 0
        while not equal(prev):
            print("iteration", cnt)
            cnt += 1
            prev = self.module_manager.get_internal_modules().copy()
            for local in self.module_manager.get_internal_modules().copy():
                analyze_local(local)
        pass

    def is_builtin(self, name):
        return name in __builtins__

    def _get_target_ns(self, target):
        if isinstance(target, ast.Name):
            id = target.id
            return [utils.join_ns(self.current_ns, id)]
        if isinstance(target, ast.Attribute):
            bases = self._get_target_ns(target.value)
            res = []
            for base in bases:
                if not base:
                    continue
                res.append(utils.join_ns(base.get_ns(), target.attr))
            return res
        if isinstance(target, ast.Subscript):
            return self.retrieve_subscript_names(target)
        return []

    def get_or_create(self, ns, x, def_type):
        defi = self.def_manager.get(utils.join_ns(ns, x))
        if not defi:
            defi = self.def_manager.getOrCreate(utils.join_ns(ns, x), def_type)
        nsScope: ScopeItem = self.scope_manager.get_scope(ns)
        if not nsScope:
            return None
        nsScope.add_def(x, defi)
        return defi

    def _handle_ns(self):
        tmpStack = self.callStack[:]
        curNsDefi: Definition = self.def_manager.get(tmpStack[-1])
        while curNsDefi.get_type() in [
            utils.constants.IF_DEF,
            utils.constants.ELSE_DEF,
            utils.constants.WHILE_DEF,
        ]:
            tmpStack.pop()
            curNsDefi = self.def_manager.get(tmpStack[-1])
        finalNs = curNsDefi.get_ns()
        return finalNs

    def mergeIfElse(self, ifFullNs, elseFullNs, row):
        ifChange, elseChange = self.change_manager.getChange(
            ifFullNs
        ), self.change_manager.getChange(elseFullNs)
        returnChangeItem = {}
        if not ifChange and not elseChange:
            pass
        elif not elseChange and ifChange:
            for defi, item in ifChange.items():
                returnChangeItem[defi] = ChangeItem(row, item.get_last_point_value())
                pass
        elif not ifChange and elseChange:
            for defi, item in elseChange.items():
                returnChangeItem[defi] = ChangeItem(row, item.get_last_point_value())
        else:
            keys = ifChange.keys() | elseChange.keys()
            for key in keys:
                if key in ifChange and key in elseChange:
                    ifChangeItem: ChangeItem = ifChange[key]
                    elseChangeItem: ChangeItem = elseChange[key]
                    tmpChangeItem = ChangeItem(
                        row,
                        ifChangeItem.get_last_point_value()
                        | elseChangeItem.get_last_point_value(),
                    )
                    returnChangeItem[key] = tmpChangeItem
                elif key in ifChange:
                    tmpChangeItem = ChangeItem(
                        row, ifChange[key].get_last_point_value(), True
                    )
                    returnChangeItem[key] = tmpChangeItem
                else:
                    tmpChangeItem = ChangeItem(
                        row, elseChange[key].get_last_point_value(), True
                    )
                    returnChangeItem[key] = tmpChangeItem
        ifScope: ScopeItem = self.scope_manager.get_scope(ifFullNs)
        elseScope: ScopeItem = self.scope_manager.get_scope(elseFullNs)
        if ifScope and not elseScope:
            for defi in ifScope.get_defs():
                changeNs = utils.join_ns(self.current_ns, defi)
                changePoint = ifScope.get_def(defi).get_last_point_value()
                returnChangeItem[changeNs] = ChangeItem(row, changePoint)
        elif elseScope and not ifScope:
            for defi in elseScope.get_defs():
                changeNs = utils.join_ns(self.current_ns, defi)
                changePoint = elseScope.get_def(defi).get_last_point_value()
                returnChangeItem[changeNs] = ChangeItem(row, changePoint)
        elif elseScope and ifScope:
            keys = ifScope.get_defs().keys() | elseScope.get_defs().keys()
            for key in keys:
                tmpKey = utils.join_ns(self.current_ns, key)
                if key in ifScope.get_defs() and key in elseScope.get_defs():
                    returnChangeItem[tmpKey] = ChangeItem(
                        row,
                        ifScope.get_def(key).get_last_point_value()
                        | elseScope.get_def(key).get_last_point_value(),
                    )
                elif key in ifScope.get_defs():
                    returnChangeItem[tmpKey] = ChangeItem(
                        row, ifScope.get_def(key).get_last_point_value()
                    )
                elif key in elseScope.get_defs():
                    returnChangeItem[tmpKey] = ChangeItem(
                        row, elseScope.get_def(key).get_last_point_value()
                    )
        return returnChangeItem

    def update(self, row, changeList: dict):
        curNsDefi: Definition = self.def_manager.get(self.current_ns)
        if curNsDefi.get_type() not in [
            utils.constants.IF_DEF,
            utils.constants.WHILE_DEF,
            utils.constants.ELSE_DEF,
        ]:
            for changedDefiNs, change in changeList.items():
                changedDefi: Definition = self.def_manager.get(changedDefiNs)
                if not changedDefi:
                    changedDefi = self.def_manager.create(
                        changedDefiNs, utils.constants.NAME_DEF
                    )
                changedDefi.add_value_point(row, change.get_last_point_value())
                curScopeNs = self.get_scope_ns(changedDefiNs)
                curScope: ScopeItem = self.scope_manager.get_scope(curScopeNs)
                if curScope:
                    curScope.add_def(changedDefiNs[len(curScopeNs) + 1:], changedDefi)
            return
        curChange: dict = self.change_manager.getChange(self.current_ns)
        for defiNs, changePoint in changeList.items():
            if defiNs in curChange:
                if changePoint.if_union:
                    curChange[defiNs].addPoint(
                        row,
                        changePoint.get_last_point_value()
                        | changePoint.get_last_point_value(),
                    )
                else:
                    curChange[defiNs].addPoint(row, changePoint.get_last_point_value())
            else:
                curChange[defiNs] = ChangeItem(row, changePoint.get_last_point_value())
            changedDefi: Definition = self.def_manager.get(defiNs)
            if not changedDefi:
                changedDefi = self.def_manager.create(defiNs, utils.constants.NAME_DEF)
            changedDefi.add_value_point(row, changePoint.get_last_point_value())
            curScopeNs = self.get_scope_ns(defiNs)
            curScope: ScopeItem = self.scope_manager.get_scope(curScopeNs)
            if curScope:
                curScope.add_def(defiNs[len(curScopeNs) + 1:], changedDefi)

    def resolve(self, calleeNs: str, row: int, flag=False) -> list:
        if "__iter__.<return>" in calleeNs:
            print()
        calleeDefi: Definition = self.def_manager.get(calleeNs)
        tmp = reduce(
            lambda x, y: x or y, map(lambda x: x in calleeNs, utils.constants.BUILTTYPE)
        )
        if not calleeDefi and tmp:
            return [calleeNs]
        if not calleeDefi:
            return [calleeNs]
        if not calleeDefi or calleeDefi.get_type() in [
            utils.constants.NAME_DEF,
            utils.constants.NA_DEF,
            utils.constants.PARAM_DEF,
            utils.constants.RETURN_DEF,
        ]:
            nsList = self.get_point(calleeNs, row)
            return list(set(nsList))
        if not calleeDefi:
            return []
        if calleeDefi.get_type() in [utils.constants.FUN_DEF, utils.constants.EXT_DEF]:
            return [calleeNs]
        if calleeDefi.get_type() == utils.constants.CLS_DEF:
            return (
                [utils.join_ns(calleeNs, utils.constants.CLS_INIT)]
                if flag
                else [calleeNs]
            )
        elif calleeDefi.get_type() == utils.constants.INT_DEF:
            return ["<int>"]
        elif calleeDefi.get_type() == utils.constants.STR_DEF:
            return ["<str>"]
        elif calleeDefi.get_type() == utils.constants.LIST_DEF:
            # return ["<list>"]
            return [calleeNs]
        elif calleeDefi.get_type() == utils.constants.MAP_DEF:
            return [calleeNs]
            return ["<map>"]
        else:
            return [calleeNs]

    def get_point(self, ns, row=0):
        def helper(ns: str):
            rightList = []
            defi: Definition = self.def_manager.get(ns)
            while not defi or defi.get_type() in [
                utils.constants.NA_DEF,
                utils.constants.PARAM_DEF,
                utils.constants.RETURN_DEF,
            ]:
                rIndex = ns.rfind(".")
                if rIndex == -1:
                    break
                rightList.insert(0, ns[rIndex:])
                ns = ns[:rIndex]
                defi = self.def_manager.get(ns)
            rIndex = ns.rfind(".")
            if rIndex != -1:
                rightList.insert(0, ns[rIndex:])
                ns = ns[:rIndex]
            return [ns], rightList
        if "__iter__.<RETURN>" in ns:
            print()
        if not isinstance(ns, str):
            return []
        leftList, rightList = helper(ns)
        while rightList:
            leftList = list(
                map(lambda x: self.mergeLeftRight(x, row, rightList[0]), leftList)
            )
            rightList.remove(rightList[0])
            leftList = self.flatten(list(map(self.convert, leftList)))
        if not leftList:
            return leftList
        leftList = list(
            filter(lambda x: x, self.flatten(list(map(self.convert_final, leftList))))
        )
        for x in leftList:
            if "__iter__.<RETURN>" in x:
                print()
        return leftList

    def mergeLeftRight(self, left, row, right):
        if left in ["<map>", "<int>", "<str>", "<list>"]:
            return left
        right = right[1:]
        leftScope: ScopeItem = self.scope_manager.get_scope(left)
        if leftScope:
            if self.find_field(left, right):
                return self.find_field(left, right).get_ns()
        ns = utils.join_ns(left, right)
        defi = self.def_manager.get(ns)
        if defi:
            return defi.get_ns()
        return ns

    def convert(self, curStr):
        def dfs(curStr: str):
            queue = [curStr]
            visited = set()
            while queue:
                cur = queue[0]
                queue.remove(cur)
                if cur in ["<map>", "<int>", "<str>", "<list>"]:
                    visited.add(cur)
                    continue
                curDefi: Definition = self.def_manager.get(cur)
                if not curDefi:
                    visited.add(cur)
                    continue
                if curDefi.get_type() in [
                    utils.constants.NAME_DEF,
                    utils.constants.NA_DEF,
                    utils.constants.PARAM_DEF,
                    utils.constants.RETURN_DEF,
                ]:
                    PointValueList = curDefi.get_last_point_value()
                    visited = visited.union(set(PointValueList))
                    for pointValue in PointValueList:
                        if pointValue not in visited:
                            queue.append(pointValue)
                    continue
                if curDefi.get_type() == utils.constants.INT_DEF:
                    visited.add("<int>")
                if curDefi.get_type() == utils.constants.STR_DEF:
                    visited.add("<str>")
                if curDefi.get_type() == utils.constants.LIST_DEF:
                    visited.add("<list>")
                if curDefi.get_type() == utils.constants.MAP_DEF:
                    visited.add("<map>")
                if "<str>" in curDefi.get_ns():
                    visited.add("<str>")
                if "<list>" in curDefi.get_ns():
                    visited.add("<list>")
                if "<dict>" in curDefi.get_ns():
                    visited.add("<dict>")
                if "<int>" in curDefi.get_ns():
                    visited.add("<int>")
                visited.add(cur)
            return visited

        if curStr in ["<map>", "<int>", "<str>", "<list>"]:
            return [curStr]
        curDefi: Definition = self.def_manager.get(curStr)
        if not curDefi and curStr in self.change_manager.getChange(self.current_ns):
            changedItem: ChangeItem = self.change_manager.getChange(self.current_ns)[
                curStr
            ]
            res = []
            pointValueList = changedItem.get_last_point_value()
            for point in pointValueList:
                if point in res:
                    continue
                # res += self.convert(point)
                res += dfs(point)
            return list(set(res))
        if not curDefi:
            return [curStr]
        if curDefi.get_type() in [
            utils.constants.NAME_DEF,
            utils.constants.NA_DEF,
            utils.constants.PARAM_DEF,
            utils.constants.RETURN_DEF,
        ]:
            curDefiList = curDefi.get_last_point_value()
            if curStr in self.change_manager.getChange(self.current_ns):
                curDefiList = (
                        curDefiList
                        | self.change_manager.getChange(self.current_ns)[
                            curStr
                        ].get_last_point_value()
                )
            nsList = []
            for curDefiNs in curDefiList:
                # tmpList = self.convert(curDefiNs)
                tmpList = dfs(curDefiNs)
                for tmp in tmpList:
                    if tmp in nsList:
                        continue
                    else:
                        nsList.append(tmp)
                nsList = list(set(nsList))
            return nsList
        if curDefi.get_type() == utils.constants.INT_DEF:
            return ["<int>"]
        if curDefi.get_type() == utils.constants.STR_DEF:
            return ["<str>"]
        if curDefi.get_type() == utils.constants.LIST_DEF:
            return ["<list>"]
        if curDefi.get_type() == utils.constants.MAP_DEF:
            return ["<map>"]
        return [curStr]

    def convert_final(self, curStr):
        curDefi: Definition = self.def_manager.get(curStr)
        tmp = reduce(
            lambda x, y: x or y, map(lambda x: x in curStr, utils.constants.BUILTTYPE)
        )
        if not curDefi and tmp:
            return curStr
        if not curDefi:
            return None
        if curDefi.get_type() in [
            utils.constants.NAME_DEF,
            utils.constants.PARAM_DEF,
            utils.constants.RETURN_DEF,
        ]:
            curDefiList = curDefi.get_last_point_value()
            nsList = []
            for curDefiNs in curDefiList:
                if curStr == curDefiNs:
                    continue
                nsList.append(curDefiNs)
            return nsList
        if curDefi.get_type() == utils.constants.INT_DEF:
            return "<int>"
        if curDefi.get_type() == utils.constants.STR_DEF:
            return "<str>"
        if curDefi.get_type() == utils.constants.LIST_DEF:
            return curStr
            return "<list>"
        if curDefi.get_type() == utils.constants.MAP_DEF:
            return curStr
            return "<map>"
        if curDefi.get_type() == utils.constants.NA_DEF:
            return None
        return curStr

    def get_module_ns(self, ns):
        defi: Definition = self.def_manager.get(ns)
        while not defi or defi.get_type() != utils.constants.MOD_DEF:
            ns = ns[: ns.rfind(".")]
            if not ns:
                break
            defi = self.def_manager.get(ns)
        return ns

    def get_scope_ns(self, ns):
        while ns and not ns in self.scope_manager.get_scopes():
            ns = ns[: ns.rfind(".")]
        return ns if ns else None

    def find_field(self, scopeNs, field):
        if scopeNs in ["<str>", "<list>", "<map>", "<int>"]:
            if scopeNs == "<str>":
                if hasattr(str, field):
                    return utils.join_ns(scopeNs, field)
            if scopeNs == "<list>":
                if hasattr(list, field):
                    return utils.join_ns(scopeNs, field)
            if scopeNs == "<map>":
                if hasattr(dict, field):
                    return utils.join_ns(scopeNs, field)
            if scopeNs == "<int>":
                if hasattr(int, field):
                    return utils.join_ns(scopeNs, field)
            return None
            # return utils.join_ns(scopeNs,field)
        scope: ScopeItem = self.scope_manager.get_scope(scopeNs)
        scopeDefi: Definition = self.def_manager.get(scopeNs)
        if not scope and scopeDefi == utils.constants.EXT_DEF:
            return utils.join_ns(scopeNs, field)
        defi: Definition = self.def_manager.get(scopeNs)
        if not scope:
            return None
        if not defi:
            return None
        if defi.get_type() == utils.constants.CLS_DEF:
            return self.find_cls_fun_ns(scopeNs, field)
        return scope.get_def(field)

    def find_cls_fun_ns(self, clsNs, fn):
        clsNode: ClassNode = self.class_manager.get(clsNs)
        for tmpClsNs in clsNode.mro:
            tmpScope: ScopeItem = self.scope_manager.get_scope(tmpClsNs)
            if not tmpScope:
                continue
            if tmpScope.get_def(fn):
                selfDefi: Definition = tmpScope.get_def("self")
                if not selfDefi:
                    continue
                selfDefi.add_value_point(0, clsNs)
                return tmpScope.get_def(fn)
        return None
        pass

    def iSDefiInScope(self, defins: Definition, scopens: ScopeItem):
        defi = self.def_manager.get(defins)
        scope = self.scope_manager.get_scope(scopens)
        for name, scopeDefi in scope.get_defs().items():
            if defi == scopeDefi:
                return True
        return False

    def retrieve_subscript_names(self, node, literFlag=False):
        if not isinstance(node, ast.Subscript):
            raise Exception("The node is not an subcript")
        if getattr(node.slice, "value", None) is not None and self._is_literal(node.slice.value):
            sl_names = [node.slice.value]
        else:
            sl_names = self.decode_node(node.slice)

        val_names = self.decode_node(node.value)

        decoded_vals = set()
        keys = set()
        full_names = set()
        # get all names associated with this variable name
        for n in val_names:
            if n and isinstance(n, Definition):
                # decoded_vals |= self.closured.get(n.get_ns())
                decoded_vals.add(n.get_ns())
        for s in sl_names:
            if isinstance(s, Definition):
                keys.add(s.get_ns())
            elif isinstance(s, str):
                keys.add(s)
            elif isinstance(s, int):
                keys.add(s)
        returnDefins = set()
        for d in decoded_vals:
            definsList = self.resolveList(d, node.lineno)
            for defins in definsList:
                defi: Definition = self.def_manager.get(defins)
                if defi and defi.get_type() in [utils.constants.LIST_DEF, utils.constants.MAP_DEF]:
                    if hasattr(defi, 'memo'):
                        defiList = set(reduce(lambda x, y: x + y, defi.memo.values()))

                        # defiList = set(map(lambda x:self.resolveList(x,node.lineno),defiList))
                        returnDefins = returnDefins.union(defiList)
                elif defi:
                    returnDefins.add(defins)
            # for key in keys:
            #     # check for existence of var name and key combination
            #     definsList = self.resolve(d,node.lineno)
            #     for defins in definsList:
            #         defi:Definition = self.def_manager.get(defins)
            #         if defi and defi.get_type() == utils.constants.LIST_DEF:
            #             # defi:Definition = self.def_manager.get(defins)
            #             # if not defi:
            #             #     continue
            #             defiList = defi.get_element(key)
            #             # defiList = set(map(lambda x:self.resolveList(x,node.lineno),defiList))
            #             returnDefins = returnDefins.union(set(defiList))

        return returnDefins


    def resolveList(self, calleeNs: str, row: int, flag=False) -> list:
        calleeDefi: Definition = self.def_manager.get(calleeNs)
        if not calleeDefi:
            return []
        if not calleeDefi or calleeDefi.get_type() in [utils.constants.NAME_DEF, utils.constants.NA_DEF,
                                                       utils.constants.PARAM_DEF, utils.constants.RETURN_DEF]:
            # nsList = self.get_point(calleeNs, row)
            # get_last_point_value
            nsList = calleeDefi.get_last_point_value()
            if not nsList:
                return []
            return reduce(lambda x, y: x + y, map(lambda x: self.resolveList(x, row), nsList))
        # elif calleeDefi.get_type() == utils.constants.LIST_DEF:
        #     # memoDict = getattr(calleeDefi,'memo',{})
        #     # pointList = list(reduce(lambda x, y: x + y, memoDict.values()))
        #     # pointList = list(reduce(lambda x, y: x + y, calleeDefi.memo.values()))
        #     # return reduce(lambda x, y: x or y, map(lambda x: self.resolveList(x, row), pointList))
        #     # return ['<list>']
        # elif calleeDefi.get_type() == utils.constants.MAP_DEF:
        #     # pointList = list(reduce(lambda x, y: x + y, calleeDefi.memo.values()))
        #     # return reduce(lambda x, y: x or y, map(lambda x: self.resolveList(x, row), pointList))
        #     # return ['<map>']
        else:
            return [calleeNs]
