





## 1. environments



Python=3.8



## 2. Usage

```shell
~ >>> python3 jarvis_cli.py -h
usage: jarvis_cli.py [-h] [--package PACKAGE] [--decy] [--precision]
                     [--moduleEntry [MODULEENTRY ...]]
                     [--operation {call-graph,key-error}] [-o OUTPUT]
                     [module ...]

positional arguments:
  module                modules to be processed

options:
  -h, --help            show this help message and exit
  --package PACKAGE     Package containing the code to be analyzed
  --decy                whether analyze the dependencies
  --precision           whether flow-sensitive
  --moduleEntry [MODULEENTRY ...]
                        Entry functions to be processed
  -o OUTPUT, --output OUTPUT
                        Output path
```




## 3. Run Jarvis

```shell
cd Jarvis
python jarvis_cli.py [module_path1 module_path2 module_path3...] [--package] [-o output_path]
```



## 4. Call Graph Output

The call edges are in the form of an adjacency list where an edge `(src, dst)` is represented as an entry of `dst` in the list assigned to key `src`:

```json
{
    "node1": ["node2", "node3"],
    "node2": ["node3"],
    "node3": []
}
```

- Node1 is a function that invokes Node2 and Node3.
- Node2 is a function that invokes Node3.
- Node3 is a function that is not invoked by any other functions in this context.



## 5. Examples

工具Jarvir提供给用户两种分析能力

1. (默认) 仅仅分析本地模块，即用户传入的modules
2. (--decy) 设置decy选项，除了分析本地模块，还会分析依赖模块。PS：你需要确定当前运行Python的虚拟环境中有这个依赖模块，否则Jarvis无法得到依赖模块

分析本地bpytop

```shell
~ >>> python3 jarvis_cli.py dataset/macro-benchmark/pj/bpytop/bpytop.py --package dataset/macro-benchmark/pj/bpytop -o jarvis.json
```



分析本地bpytop+依赖模块

```shell
# install Dependencies in virtualenv environment
~ >>> python3 -m pip install psutil
~ >>> python3 jarvis_cli.py dataset/macro-benchmark/pj/bpytop/bpytop.py --package dataset/macro-benchmark/pj/bpytop --decy -o jarvis.json
```





## 6. Running benchmark

得到benchmark的结果





