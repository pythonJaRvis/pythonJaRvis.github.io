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

import argparse
import time
import formats
from jarvis import CallGraphGenerator
from utils.constants import CALL_GRAPH_OP, KEY_ERR_OP
import json


def main():
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("entry_point",
                        nargs="*",
                        help="Entry points to be processed")
    parser.add_argument(
        "--package",
        help="Package containing the code to be analyzed",
        default=None
    )
    parser.add_argument(
        "--decy",
        action="store_true",
        help="whether iterate the dependency",
        default=False
    )
    parser.add_argument(
        "--precision",
        action="store_true",
        help="whether flow-sensitive",
        default=False
    )
    parser.add_argument(
        "--moduleEntry",
        nargs="*",
        help="whether make main as entry",
        default=None
    )
    parser.add_argument(
        '--operation',
        type=str,
        choices=[CALL_GRAPH_OP, KEY_ERR_OP],
        help=("Operation to perform. " +
              "Choose " + CALL_GRAPH_OP + " for call graph generation (default)" +
              " or " + KEY_ERR_OP + " for key error detection on dictionaries."),
        default=CALL_GRAPH_OP
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output path",
        default=None
    )
    args = parser.parse_args()
    if not args.entry_point:
        raise Exception("Need entry_point")
    cg = CallGraphGenerator(args.entry_point, args.package,args.operation, decy=args.decy,precision=args.precision, moduleEntry=args.moduleEntry)
    cg.analyze()

    formatter = formats.Fasten(cg, '',)
    formatter = formats.Simple(cg)
    output = formatter.generate()
    output = formatter.generate()
    as_formatter = formats.AsGraph(cg)

    if args.output:
        with open(args.output, "w+") as f:
            f.write(json.dumps(output))
    else:
        print(json.dumps(output))


if __name__ == '__main__':
    main()
