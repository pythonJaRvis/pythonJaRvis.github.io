import os

import os
import json

curcwd = os.getcwd()
base = os.path.join(curcwd,'reproducing_RQ1','macro_benchmark')
pjList = ['bpytop', 'sqlparse', 'textrank4zh', 'furl', 'rich-cli', 'sshtunnel']

def getTime(pj):
    res = []

    def process(lines):
        time = None
        mem = None
        lines = lines.split('\n')
        for line in lines:
            if line.startswith("real"):
                res = line.replace("real", '')
                res = float(res)
                time = round(res, 2)
            if line.endswith("maximum resident set size"):
                res = line.replace("maximum resident set size", '')
                res = float(res)
                mem = round(res / (1024 ** 2))
            try:
                time = round(float(line), 2)
            except:
                continue
        return time, mem

    path = os.path.join(base, pj, 'pycg-log', 'pycg_EA(1).log')
    with open(path, 'r') as f:
        lines = f.read()
        tmp = (process(lines))
        res.append(tmp[0])
        res.append(tmp[1])
    path = os.path.join(base, pj, 'pycg-log', 'pycg_EA(m).log')
    with open(path, 'r') as f:
        lines = f.read()
        tmp = (process(lines))
        res.append(tmp[0])
        res.append(tmp[1])

    path = os.path.join(base, pj, 'pycg-log', 'pycg_EW(1).log')
    with open(path, 'r') as f:
        lines = f.read()
        tmp = (process(lines))
        res.append(tmp[0])
        res.append(tmp[1])

    path = os.path.join(base, pj, 'pycg-log', 'pycg_EW(2).log')
    with open(path, 'r') as f:
        lines = f.read()
        tmp = (process(lines))
        res.append(tmp[0])
        res.append(tmp[1])

    path = os.path.join(base, pj, 'pycg-log', 'pycg_EW(m).log')
    if not os.path.exists(path):
        res.append('----')
        res.append('----')
    else:
        with open(path, 'r') as f:
            lines = f.read()
            tmp = (process(lines))
            res.append(tmp[0])
            res.append(tmp[1])

    path = os.path.join(base, pj, 'jarvis-log', 'jarvis_EA.log')
    with open(path, 'r') as f:
        lines = f.read()
        tmp = (process(lines))
        res.append(tmp[0])
        res.append(tmp[1])

    path = os.path.join(base, pj, 'jarvis-log', 'jarvis_EW.log')
    with open(path, 'r') as f:
        lines = f.read()
        tmp = (process(lines))
        res.append(tmp[0])
        res.append(tmp[1])
    path = os.path.join(base, pj, 'jarvis-log', 'jarvis_DA.log')
    with open(path, 'r') as f:
        lines = f.read()
        tmp = (process(lines))
        res.append(tmp[0])
        res.append(tmp[1])
    path = os.path.join(base, pj, 'jarvis-log', 'jarvis_DW.log')
    with open(path, 'r') as f:
        lines = f.read()
        tmp = (process(lines))
        res.append(tmp[0])
        res.append(tmp[1])

    # print(" ".join(map(str, res)))
    return res
totalres = []
for pj in pjList:
    res = getTime(pj)
    totalres.append(res)

s = '''
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------
|{}        {}                {}
|{} {} {} {} {} {} {} {} {} {} {}
|{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}
|{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}
|{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}
|{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}
|{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}
|{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}
|{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}
'''
interval = 80
int1 = 8
cur = [
    ' Id.'.center(int1), 'PYCG'.center(interval), 'JARVIS'.center(interval // 2),
    '  '.center(int1), 'E.A.(1).'.center(int1*2), 'E.A.(m).'.center(int1*2), 'E.W.(1)'.center(int1*2), 'E.W.(2)'.center(int1*2),'E.W.(m)'.center(int1*2), 'A.W.(2)'.center(int1*2), 'E.A.'.center(int1*2), 'E.W.'.center(int1*2), 'A.A.'.center(int1*2),'A.W.'.center(int1*2),
    ''.center(int1),'T.'.center(int1),'M.'.center(int1),'T.'.center(int1),'M.'.center(int1),'T.'.center(int1),'M.'.center(int1),'T.'.center(int1),'M.'.center(int1),'T.'.center(int1),'M.'.center(int1),'T.'.center(int1),'M.'.center(int1),'T.'.center(int1),'M.'.center(int1),'T.'.center(int1),'M.'.center(int1),'T.'.center(int1),'M.'.center(int1)
]

for i in range(len(pjList)):
    cur.append("P{}".format(i+1).center(int1))
    cur += list(map(lambda x:str(x).center(int1),totalres[i]))
s = s.format(*cur)
print(s)