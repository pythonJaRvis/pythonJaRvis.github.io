
import os
import sys
import importlib
import json

from unittest import TestCase, main
import utils


class TestBase(TestCase):
    snippet_dir = ""

    def setUp(self):
        def error():
            print ("Invalid module %s.%s" % (cg_mod, cg_class))
            print ("Set environment variables `CALL_GRAPH_CLASS` and `CALL_GRAPH_MODULE` properly")
            sys.exit(1)

        # self.snippets_path = os.environ.get("SNIPPETS_PATH")
        self.snippets_path = '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets'
        # cg_class = os.environ.get('CALL_GRAPH_CLASS', None)
        # cg_mod = os.environ.get('CALL_GRAPH_MODULE', None)
        cg_class = "CallGraphGenerator"
        cg_mod = "pythoncg"
        # cg_mod = os.environ.get('CALL_GRAPH_MODULE', None)
        if not cg_class or not cg_mod:
            error()
        try:
            self.cg_mod = importlib.import_module(cg_mod)
        except ImportError:
            error()

        self.cg_class = getattr(self.cg_mod, cg_class)
        if not self.cg_class:
            error()

    def validate_snippet(self, snippet_path):
        output = self.get_snippet_output_cg(snippet_path)
        expected = self.get_snippet_expected_cg(snippet_path)

        self.assertEqual(output, expected)

    def get_snippet_path(self, name):
        return os.path.join(self.snippets_path, self.snippet_dir, name)

    def get_snippet_output_cg(self, snippet_path):
        main_path = os.path.join(snippet_path, "main.py")
        try:
            # cg = self.cg_class([main_path], snippet_path, -1, utils.constants.CALL_GRAPH_OP)
            cg = self.cg_class([main_path], snippet_path, -1, utils.constants.CALL_GRAPH_OP,precision = True)
            cg.analyze()
            output =cg.output()
            output_cg = {}
            for node in output:
                output_cg[node] = list(output[node])
            with open(os.path.join(snippet_path,'pythonCG.json'),'w') as f:
                json.dump(output_cg,f)
                # f.write(json.dumps(cg.output()))
            return output
        except Exception as e:
            cg.tearDown()
            raise e

    def get_snippet_expected_cg(self, snippet_path):
        cg_path = os.path.join(snippet_path, "callgraph.json")
        with open(cg_path, "r") as f:
            return json.loads(f.read())

    def assertEqual(self, actual, expected):
        def do_sorted(d):
            s = {}
            for n in d:
                if not d[n]:
                    continue
                s[n] = sorted(d[n])
            return s

        super().assertEqual(do_sorted(actual), do_sorted(expected))


if __name__ == "__main__":
    main()
