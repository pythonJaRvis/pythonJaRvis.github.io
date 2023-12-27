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

import json
import os

from processing.extProcessor import ExtProcessor
from machinery.scopes import ScopeManager, ScopeItem
from machinery.definitions import (
    DefinitionManager,
    Definition,
    ChangeManager,
    ChangeItem,
)
from machinery.imports import ImportManager
from machinery.classes import ClassManager, ClassNode
from machinery.returns import ReturnManager
from machinery.callgraph import CallGraph
from machinery.modules import ModuleManager
from machinery.nodes import NodeManager
from machinery import gol
import utils


class CallGraphGenerator(object):
    def __init__(
        self,
        entry_points,
        package,
        decy=False,
        moduleEntry=[],
        precision=False
    ):
        self.entry_points = entry_points
        self.package = package
        self.state = None
        self.decy = decy
        self.moduleEntry = moduleEntry
        self.precision = precision
        self.setUp()

    def setUp(self):
        self.import_manager = ImportManager()
        self.scope_manager = ScopeManager()
        self.def_manager = DefinitionManager()
        self.class_manager: ClassManager = ClassManager()
        self.module_manager = ModuleManager()
        self.change_manager = ChangeManager()
        self.return_manager = ReturnManager()
        self.cg = CallGraph()
        self.node_manager: NodeManager = NodeManager()
        gol._init()
        if self.precision:
            gol.set_value("precision", self.precision)

    def extract_state(self):
        state = {}
        state["defs"] = {}
        for key, defi in self.def_manager.get_defs().items():
            state["defs"][key] = {
                "names": defi.get_name_pointer().get().copy(),
                "lit": defi.get_lit_pointer().get().copy(),
            }

        state["scopes"] = {}
        for key, scope in self.scope_manager.get_scopes().items():
            state["scopes"][key] = set(
                [x.get_ns() for (_, x) in scope.get_defs().items()]
            )

        state["classes"] = {}
        for key, ch in self.class_manager.get_classes().items():
            state["classes"][key] = ch.get_mro().copy()
        return state

    def reset_counters(self):
        for key, scope in self.scope_manager.get_scopes().items():
            scope.reset_counters()

    def remove_import_hooks(self):
        self.import_manager.remove_hooks()

    def _get_mod_name(self, entry, pkg):
        input_mod = utils.to_mod_name(os.path.relpath(entry, pkg))
        if input_mod.endswith("__init__"):
            input_mod = ".".join(input_mod.split(".")[:-1])

        return input_mod

    def do_pass(
        self, cls, install_hooks=False, modules_analyzed=set(), *args, **kwargs
    ):
        modules_analyzed = modules_analyzed
        processor: ExtProcessor = None
        input_pkg = None
        for entry_point in self.entry_points:
            input_pkg = self.package
            input_mod = self._get_mod_name(entry_point, input_pkg)
            input_file = os.path.abspath(entry_point)
            if not input_mod:
                continue
            if not input_pkg:
                input_pkg = os.path.dirname(input_file)
            if install_hooks:
                self.import_manager.set_pkg(input_pkg)
                self.import_manager.install_hooks()
            processor = cls(
                input_file,
                input_mod,
                modules_analyzed=modules_analyzed,
                decy=self.decy,
                *args,
                **kwargs
            )
            self.module_manager.add_local_modules(input_mod)
            processor.analyze()
            modules_analyzed = modules_analyzed.union(processor.get_modules_analyzed())
            if install_hooks:
                self.remove_import_hooks()
        if install_hooks:
            self.import_manager.set_pkg(input_pkg)
            self.import_manager.install_hooks()
        if not self.moduleEntry:
            self.moduleEntry = []
            for local in self.module_manager.local:
                moduleNode = self.module_manager.get(local)
                if not moduleNode:
                    continue
                methodDict: dict = moduleNode.get_methods()
                for method in methodDict.keys():
                    self.moduleEntry.append(method)
        processor.analyze_localfunction(self.moduleEntry)

    def analyze(self):
        import time

        start = time.time()
        gol.set_value('cnt',0)
        self.do_pass(
            ExtProcessor,
            True,
            set(),
            self.import_manager,
            self.scope_manager,
            self.def_manager,
            self.class_manager,
            self.module_manager,
            self.change_manager,
            self.node_manager,
            self.cg,
        )
        end = time.time()

    def output(self):
        return self.cg.get()

    def output_key_errs(self):
        return self.key_errs.get()

    def output_edges(self):
        return self.key_errors

    def output_edges(self):
        return self.cg.get_edges()

    def _generate_mods(self, mods):
        res = {}
        for mod, node in mods.items():
            res[mod] = {
                "filename": os.path.relpath(node.get_filename(), self.package)
                if node.get_filename()
                else None,
                "methods": node.get_methods(),
            }
        return res

    def output_internal_mods(self):
        return self._generate_mods(self.module_manager.get_internal_modules())

    def output_external_mods(self):
        return self._generate_mods(self.module_manager.get_external_modules())

    def output_functions(self):
        functions = []
        for ns, defi in self.def_manager.get_defs().items():
            if defi.is_function_def():
                functions.append(ns)
        return functions

    def output_classes(self):
        classes = {}
        for cls, node in self.class_manager.get_classes().items():
            classes[cls] = {
                "mro": node.get_mro(),
                "module": node.get_module(),
            }
        return classes

    def get_as_graph(self):
        return self.def_manager.get_defs().items()
