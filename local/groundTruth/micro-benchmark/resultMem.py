import os


def getMem(pycgPath,pythonPath):
    pycgmem = 0
    pythonmem = 0
    with open(pycgPath,'r') as f:
        lines = f.read().split('\n')
    for line in lines:
        line = line.strip()
        # print(line)
        if line.endswith("maximum resident set size"):
            res = line.replace("maximum resident set size",'')
            res = int(res)
            pycgmem = res
    with open(pythonPath,'r') as f:
        lines = f.read().split('\n')
    for line in lines:
        line = line.strip()
        # print(line)
        if line.endswith("maximum resident set size"):
            res = line.replace("maximum resident set size",'')
            res = int(res)
            pythonmem = res      
            break
    return pycgmem,pythonmem
def findFile(base):
    for root, ds, fs in os.walk(base):
        returnList = [0] * 2
        pycgPath,pythonPath = None,None
        for f in fs:
            if f == 'pycg.log':
                pycgPath = os.path.join(root, f)
            if f == 'pythoncg.log':
                pythonPath = os.path.join(root, f)
        # yield run(returnList[0] , returnList[1] , returnList[2])
        yield getMem(pycgPath,pythonPath)
        # main(returnList[0] , returnList[1]  ,returnList[2])
def process(pycg_list , pythoncg_list):
    pre_pycg = [0,0,0,0]
    pre_python = [0,0,0,0]
    pre_pycg = list(map(lambda x:x[0] + x[1] , zip(pre_pycg,pycg_list)))
    yield pre_pycg
global_pycg = 0
global_pythoncg = 0
def main(base):
    global global_pycg
    global global_pythoncg
    pre_pycg = 0
    pre_python = 0
    for root, ds, fs in os.walk(base):
        returnList = [0] * 2
        pycgPath,pythonPath = None,None
        for f in fs:
            if f == 'pycg.log':
                pycgPath = os.path.join(root, f)
            if f == 'pythoncg.log':
                pythonPath = os.path.join(root, f)
        # yield run(returnList[0] , returnList[1] , returnList[2])
        yield getMem(pycgPath,pythonPath)
    # for i in findFile(base):
    #     if not i:
    #         continue
    #     pre_pycg = list(map(lambda x:x[0] + x[1] , zip(pre_pycg,list(i[0]))))
    #     pre_python = list(map(lambda x:x[0] + x[1] , zip(pre_python,list(i[1]))))
        # print(pre_pycg,pre_python)
    pycg_str = "{},{},{}/{}".format(*pre_pycg)
    python_str = "{},{},{}/{}".format(*pre_python)
    res = pre_pycg + pre_python
    # save_xlsx(190+index,base.split(os.path.sep)[-1],res)
    print(base.split(os.path.sep)[-1])
    print(pycg_str , python_str)
    global_pycg = list(map(lambda x:x[0] + x[1] , zip(pre_pycg,global_pycg)))
    global_pythoncg = list(map(lambda x:x[0] + x[1] , zip(pre_python,global_pythoncg)))

entryes = [
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/args',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/assignments',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/builtins',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/classes',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/decorators',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/dicts',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/direct_calls',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/exceptions',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/functions',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/generators',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/imports',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/kwargs',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/lambdas',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/lists',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/mro',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/returns',


    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/newCase/args',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/newCase/assign',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/newCase/calls',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/newCase/control_flow',
    '/Users/yixuanyan/yyx/github/supplychain/YanYixuan/pythonCG/micro-benchmark/snippets/newCase/import',
]
pycgtotal =0
pythontotal = 0
for index,entry in enumerate(entryes):
    print(entry.split(os.path.sep)[-1])
    visited = set()
    pycgcur ,pythoncur = 0,0
    for root, ds, fs in os.walk(entry):
        pycgPath, pythonPath = None, None
        for f in fs:
            if f == 'pycg.log':
                pycgPath = os.path.join(root, f)
            if f == 'pythoncg.log':
                pythonPath = os.path.join(root, f)
            if pycgPath and pythonPath and (pycgPath,pythonPath) not in visited:
                pyT ,pythonT =  getMem(pycgPath, pythonPath)
                visited.add((pycgPath,pythonPath))
                pycgcur , pythoncur = pycgcur + pyT , pythoncur + pythonT
    pycgtotal , pythontotal = pycgtotal + pycgcur , pythoncur + pythontotal
    print(round(pycgcur/(1024**2)),round(pythoncur/(1024**2)))
print(round(pycgtotal/(1024**2)),round(pythontotal/(1024**2)))