import os
import json
import math

curcwd = os.getcwd()
Gt_Path = os.path.join(curcwd,'ground_truth', 'micro_benchmark')
Gt_Path = os.path.normpath(Gt_Path)
Output_Path = os.path.join(curcwd, 'reproducing_RQ2', 'micro_benchmark')


def getEdges(cg: dict):
    cnt = 0
    for k, vList in cg.items():
        cnt += len(vList)
    return cnt


def getTP(truthJson, curJson):
    cnt = 0
    for k, vList in curJson.items():
        if k in truthJson:
            cnt += len(set(vList) & set(truthJson[k]))
    return cnt


def getFN(truthJson, curJson, TP):
    return getEdges(truthJson) - TP


def getFP(truthJson, curJson, TP):
    return getEdges(curJson) - TP


def getResult(truthJson: dict, curJson: dict):
    complete, sound = 0, 0
    TP = getTP(truthJson, curJson)
    FP = getFP(truthJson, curJson, TP)
    FN = getFN(truthJson, curJson, TP)
    edges = getEdges(truthJson)
    if not FP:
        complete = 1
    if not FN:
        sound = 1
    return [TP, FP, FN, edges, complete, sound]


def findFile(item):
    def run(truth, pycg, pythoncg):
        if isinstance(truth, int) or isinstance(pycg, int) or isinstance(pycg, int):
            return
        TP, FN, FP = 0, 0, 0
        with open(truth, "r") as f:
            truthJson: dict = json.load(f)
        with open(pycg, "r") as f:
            pycgJson: dict = json.load(f)
        with open(pythoncg, "r") as f:
            pythoncgJson: dict = json.load(f)

        # Result array contains [TP, FP, FN, edges]
        pycg_res = getResult(truthJson, pycgJson)
        python_res = getResult(truthJson, pythoncgJson)
        return pycg_res, python_res

    for root, ds, fs in os.walk(os.path.join(Output_Path, item)):
        returnList = [0] * 3
        for f in fs:
            if f == "pycg.json":
                fullname = os.path.join(root, f)
                returnList[1] = fullname
                # print(root,Output_Path,Gt_Path)
                # print(root.replace(Output_Path, Gt_Path))
                fullname = os.path.join(root.replace(Output_Path, Gt_Path), 'callgraph.json')
                returnList[0] = fullname
            if f == "jarvis.json":
                fullname = os.path.join(root, f)
                returnList[2] = fullname
        yield run(returnList[0], returnList[1], returnList[2])
        # yield getMem(returnList[0], returnList[1])


global_pycg = [0, 0, 0, 0, 0, 0]
global_pythoncg = [0, 0, 0, 0, 0, 0]


def micro_table(index, item):
    global global_pycg
    global global_pythoncg
    pre_pycg = [0, 0, 0, 0, 0, 0]
    pre_python = [0, 0, 0, 0, 0, 0]
    for i in findFile(item):
        if not i:
            continue
        pre_pycg = list(map(lambda x: x[0] + x[1], zip(pre_pycg, list(i[0]))))
        pre_python = list(map(lambda x: x[0] + x[1], zip(pre_python, list(i[1]))))

    pycg_str = "{4},{5},{0},{1},{2}/{3}".format(*pre_pycg)
    python_str = "{4},{5},{0},{1},{2}/{3}".format(*pre_python)
    res = pre_pycg + pre_python
    # save_xlsx(3 + index, base.split(os.path.sep)[-1], res)
    # print(item)
    # print(f"{pycg_str} - {python_str}\n")
    global_pycg = list(map(lambda x: x[0] + x[1], zip(pre_pycg, global_pycg)))
    global_pythoncg = list(map(lambda x: x[0] + x[1], zip(pre_python, global_pythoncg)))
    return pre_pycg, pre_python


# SNIPPETS_PATH = os.environ.get("SNIPPETS_PATH")
entries = [
    f"arguments",
    f"assignments",
    f"builtins",
    f"classes",
    f"decorators",
    f"dicts",
    f"direct_calls",
    f"exceptions",
    f"functions",
    f"generators",
    f"imports",
    f"kwargs",
    f"lambdas",
    f"lists",
    f"mro",
    f"returns",
    f"context_managers",
    f"new_arguments",
    f"new_assignments",
    f"new_control_flow",
    f"new_direct_calls",
    f"new_imports"
]
nums = [6, 4, 3, 22, 7, 12, 4, 3, 4, 6, 14, 3, 5, 8, 7, 4,4, 4, 4, 4, 5, 5]

s = '''
|-------------------------------------------------------------------------------------------------------------
|{}        {}                {}
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 
|{} {} {} {} {} {} {} {} {} {} {} 


'''
interval = 40
int1 = 8
cur = [
    'Category'.center(interval // 2), 'PYCG'.center(interval), 'JARVIS'.center(interval // 2),
    ''.center(interval // 2), 'C.'.center(int1), 'S.'.center(int1), 'TP'.center(int1), 'FP'.center(int1),
    'FN'.center(int1), 'C.'.center(int1), 'S.'.center(int1), 'TP'.center(int1), 'FP'.center(int1), 'FN'.center(int1)
]

for index, (entry, num) in enumerate(zip(entries, nums)):
    if entry == 'context_managers':
        print
    pycgres, jarvisres = micro_table(index, entry)
    cur.append(entry.center(interval // 2))
    cur.append("{}/{}".format(pycgres[4], num).center(int1))
    cur.append("{}/{}".format(pycgres[5], num).center(int1))
    cur.append("{}/{}".format(pycgres[0], pycgres[3]).center(int1))
    cur.append("{}/{}".format(pycgres[1], pycgres[3]).center(int1))
    cur.append("{}/{}".format(pycgres[2], pycgres[3]).center(int1))
    cur.append("{}/{}".format(jarvisres[4], num).center(int1))
    cur.append("{}/{}".format(jarvisres[5], num).center(int1))
    cur.append("{}/{}".format(jarvisres[0], jarvisres[3]).center(int1))
    cur.append("{}/{}".format(jarvisres[1], jarvisres[3]).center(int1))
    cur.append("{}/{}".format(jarvisres[2], jarvisres[3]).center(int1))

cur.append("total".center(interval // 2))
cur.append("{}/{}".format(global_pycg[4], sum(nums)).center(int1))
cur.append("{}/{}".format(global_pycg[5], sum(nums)).center(int1))
cur.append("{}/{}".format(global_pycg[0], global_pycg[3]).center(int1))
cur.append("{}/{}".format(global_pycg[1], global_pycg[3]).center(int1))
cur.append("{}/{}".format(global_pycg[2], global_pycg[3]).center(int1))
cur.append("{}/{}".format(global_pythoncg[4], sum(nums)).center(int1))
cur.append("{}/{}".format(global_pythoncg[5], sum(nums)).center(int1))
cur.append("{}/{}".format(global_pythoncg[0], global_pythoncg[3]).center(int1))
cur.append("{}/{}".format(global_pythoncg[1], global_pythoncg[3]).center(int1))
cur.append("{}/{}".format(global_pythoncg[2], global_pythoncg[3]).center(int1))

s = s.format(*cur)
print(s)

# print("Final:")
# print(global_pycg, global_pythoncg)


import json
import os

pjList = ['bpytop', 'sqlparse', 'textrank4zh', 'furl', 'rich-cli', 'sshtunnel']



def run(truth, pycg, pythoncg):
    if isinstance(truth, int) or isinstance(pycg, int) or isinstance(pycg, int):
        return
    TP, FN, FP = 0, 0, 0
    if not (os.path.exists(truth) and os.path.exists(pycg) and os.path.exists(pythoncg)):
        return ['----']*10
    with open(truth, 'r') as f:
        truthJson: dict = json.load(f)
    with open(pycg, 'r') as f:
        pycgJson: dict = json.load(f)
    with open(pythoncg, 'r') as f:
        pythoncgJson: dict = json.load(f)
    pycg_res = getResult(truthJson, pycgJson)
    python_res = getResult(truthJson, pythoncgJson)
    # return pycg_res , python_res , pycg_res[0]/(pycg_res[0]+pycg_res[1]),pycg_res[0]/pycg_res[3] , python_res[0]/(python_res[0]+python_res[1]),python_res[0]/pycg_res[3]
    # return  pycg_res[0]/(pycg_res[0]+pycg_res[1]),pycg_res[0]/pycg_res[3] , python_res[0]/(python_res[0]+python_res[1]),python_res[0]/pycg_res[3]
    return (
        pycg_res[0], pycg_res[1], pycg_res[2],
        round(pycg_res[0] / (pycg_res[0] + pycg_res[1]),), round(pycg_res[0] / pycg_res[3],2),
        # pycg_res[0] / (pycg_res[0] + pycg_res[1]), pycg_res[0] / pycg_res[3],

        python_res[0], python_res[1], python_res[2],
        # python_res[0] / (python_res[0] + python_res[1]), python_res[0] / pycg_res[3],2)
        # round(pycg_res[0] / (pycg_res[0] + pycg_res[1]),), round(pycg_res[0] / pycg_res[3],2),
        round(python_res[0] / (python_res[0] + python_res[1]), 2), round(python_res[0] / pycg_res[3], 2))


    # 假阴 多边


def getResult(truthJson: dict, curJson: dict):
    tp = getTP(truthJson, curJson)
    edges = getEdges(truthJson)
    FP, FN = getFP(truthJson, curJson, tp), getFN(truthJson, curJson, tp)
    return [tp, FP, FN, edges]
    # return "{},{},{}/{}".format(tp,FN,FP,edges)

totalRes = []
EA1 = []
tmpRes = []

for index, pj in enumerate(pjList):
    if index == 1:
        print()
    gt = os.path.join(curcwd, 'ground_truth', 'macro_benchmark', pj)
    output = os.path.join(curcwd, 'reproducing_RQ2', 'macro_benchmark', pj)
    res = run(os.path.join(gt, 'EA.json'),
              os.path.join(output, 'pycg', 'pycg_EA(1).json'),
              os.path.join(output, 'pycg', 'pycg_EA(1).json'))
    # print(res)
    # save_xlsx(241+index,res)
    partRes = (res[8], res[9], res[8], res[9])
    EA1.append([res[8], res[9]])
    totalRes.append(EA1)
DA1 = []
for index, pj in enumerate(pjList):
    if index == 2:
        print()
    gt = os.path.join(curcwd, 'ground_truth', 'macro_benchmark', pj)
    output = os.path.join(curcwd, 'reproducing_RQ2', 'macro_benchmark', pj)
    # print(pj)
    res = run(os.path.join(gt, 'DA.json'),
              os.path.join(output, 'pycg', 'pycg_DA(1).json'),
              os.path.join(output, 'pycg', 'pycg_DA(1).json'))
    # print(res)
    # save_xlsx(241+index,res)
    partRes = (res[8], res[9], res[8], res[9])
    DA1.append([res[8], res[9]])
    totalRes.append(DA1)
EAm=[]
for index, pj in enumerate(pjList):
    gt = os.path.join(curcwd, 'ground_truth', 'macro_benchmark', pj)
    output = os.path.join(curcwd, 'reproducing_RQ2', 'macro_benchmark', pj)
    res = run(os.path.join(gt, 'EA.json'),
              os.path.join(output, 'pycg', 'pycg_EA(m).json'),
              os.path.join(output, 'pycg', 'pycg_EA(m).json'))
    # print(res)
    # save_xlsx(241+index,res)
    partRes = (res[8], res[9], res[8], res[9])
    EAm.append([res[8], res[9]])
    totalRes.append(EAm)

DAm = []
for index, pj in enumerate(pjList):
    gt = os.path.join(curcwd, 'ground_truth', 'macro_benchmark', pj)
    output = os.path.join(curcwd, 'reproducing_RQ2', 'macro_benchmark', pj)
    res = run(os.path.join(gt, 'DA.json'),
              os.path.join(output, 'pycg', 'pycg_DA(m).json'),
              os.path.join(output, 'pycg', 'pycg_DA(m).json'))
    # print(res)
    # save_xlsx(241+index,res)
    partRes = (res[8], res[9], res[8], res[9])
    DAm.append([res[8], res[9]])
    totalRes.append(DAm)

DW1=[]
for index, pj in enumerate(pjList):
    if index == 2:
        print()
    gt = os.path.join(curcwd, 'ground_truth', 'macro_benchmark', pj)
    output = os.path.join(curcwd, 'reproducing_RQ2', 'macro_benchmark', pj)
    res = run(os.path.join(gt, 'DW.json'),
              os.path.join(output, 'pycg', 'pycg_DW(1).json'),
              os.path.join(output, 'pycg', 'pycg_DW(1).json'))
    # print(res)
    # save_xlsx(241+index,res)
    partRes = (res[8], res[9], res[8], res[9])
    DW1.append([res[8], res[9]])
    totalRes.append(DW1)

DW2 = []
for index, pj in enumerate(pjList):
    gt = os.path.join(curcwd, 'ground_truth', 'macro_benchmark', pj)
    output = os.path.join(curcwd, 'reproducing_RQ2', 'macro_benchmark', pj)
    res = run(os.path.join(gt, 'DW.json'),
              os.path.join(output, 'pycg', 'pycg_DW(2).json'),
              os.path.join(output, 'pycg', 'pycg_DW(2).json'))
    # print(res)
    # save_xlsx(241+index,res)
    partRes = (res[8], res[9], res[8], res[9])
    DW2.append([res[8], res[9]])
    totalRes.append(DW2)

EA=[]
for index, pj in enumerate(pjList):
    gt = os.path.join(curcwd, 'ground_truth', 'macro_benchmark', pj)
    output = os.path.join(curcwd, 'reproducing_RQ2', 'macro_benchmark', pj)
    res = run(os.path.join(gt, 'EA.json'),
              os.path.join(output, 'jarvis', 'jarvis_EA.json'),
              os.path.join(output, 'jarvis', 'jarvis_EA.json'))
    # print(res)
    # save_xlsx(241+index,res)
    partRes = (res[8], res[9], res[8], res[9])
    EA.append([res[8], res[9]])
    totalRes.append(EA)

DA = []
for index, pj in enumerate(pjList):
    gt = os.path.join(curcwd, 'ground_truth', 'macro_benchmark', pj)
    output = os.path.join(curcwd, 'reproducing_RQ2', 'macro_benchmark', pj)
    res = run(os.path.join(gt, 'DA.json'),
              os.path.join(output, 'jarvis', 'jarvis_DA.json'),
              os.path.join(output, 'jarvis', 'jarvis_DA.json'))
    # print(res)
    # save_xlsx(241+index,res)
    partRes = (res[8], res[9], res[8], res[9])
    DA.append([res[8], res[9]])
    totalRes.append(DA)

DW=[]
for index, pj in enumerate(pjList):
    gt = os.path.join(curcwd, 'ground_truth', 'macro_benchmark', pj)
    output = os.path.join(curcwd, 'reproducing_RQ2', 'macro_benchmark', pj)
    res = run(os.path.join(gt, 'DW.json'),
              os.path.join(output, 'jarvis', 'jarvis_DW.json'),
              os.path.join(output, 'jarvis', 'jarvis_DW.json'))
    # print(res)
    # save_xlsx(241+index,res)
    partRes = (res[8], res[9], res[8], res[9])
    DW.append([res[8], res[9]])
    totalRes.append(DW)



s = '''
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------
|{}        {}                {}
|{} {} {} {} {} {} {} {} {} {}
|{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}
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
    'Id.'.center(int1), 'PYCG'.center(interval), 'JARVIS'.center(interval // 2),
    ''.center(int1+2), 'E.A.(1).'.center(int1*2), 'A.A.(1).'.center(int1*2), 'E.A.(m)'.center(int1*2), 'A.A.(m)'.center(int1*2),'A.W.(1)'.center(int1*2), 'A.W.(2)'.center(int1*2), 'E.A.'.center(int1*2), 'A.A.'.center(int1*2), 'A.W.'.center(int1*2),
    ''.center(int1), 'Pre.'.center(int1),'Rec.'.center(int1),'Pre.'.center(int1),'Rec.'.center(int1),'Pre.'.center(int1),'Rec.'.center(int1),'Pre.'.center(int1),'Rec.'.center(int1),'Pre.'.center(int1),'Rec.'.center(int1),'Pre.'.center(int1),'Rec.'.center(int1),'Pre.'.center(int1),'Rec.'.center(int1),'Pre.'.center(int1),'Rec.'.center(int1),'Pre.'.center(int1),'Rec.'.center(int1)
]

for index in range(len(pjList)):
    tmp = []
    tmp.append("P{}".format(index+1).center(int1))
    tmp.append(str(EA1[index][0]).center(int1))
    tmp.append(str(EA1[index][1]).center(int1))
    tmp.append(str(DA1[index][0]).center(int1))
    tmp.append(str(DA1[index][1]).center(int1))
    tmp.append(str(EAm[index][0]).center(int1))
    tmp.append(str(EAm[index][1]).center(int1))
    tmp.append(str(DAm[index][0]).center(int1))
    tmp.append(str(DAm[index][1]).center(int1))
    tmp.append(str(DW1[index][0]).center(int1))
    tmp.append(str(DW1[index][1]).center(int1))
    tmp.append(str(DW2[index][0]).center(int1))
    tmp.append(str(DW2[index][1]).center(int1))
    tmp.append(str(EA[index][0]).center(int1))
    tmp.append(str(EA[index][1]).center(int1))
    tmp.append(str(DA[index][0]).center(int1))
    tmp.append(str(DA[index][1]).center(int1))
    tmp.append(str(DW[index][0]).center(int1))
    tmp.append(str(DW[index][1]).center(int1))

    cur += tmp
cur.append("Aver.".center(int1))
x1,x2 = 0,0
cnt1,cnt2 = 0,0
for i in range(6):
    if isinstance(EA1[i][0],float):
        x1 += EA1[i][0]
        cnt1 += 1
    if isinstance(EA1[i][1],float):
        x2 += EA1[i][1]
        cnt2 += 1
x1,x2 = round(x1/cnt1,2),round(x2/cnt2,2)
cur.append(str(x1).center(int1))
cur.append(str(x2).center(int1))

x1,x2 = 0,0
cnt1,cnt2 = 0,0
for i in range(6):
    if isinstance(DA1[i][0],float):
        x1 += DA1[i][0]
        cnt1 += 1
    if isinstance(DA1[i][1],float):
        x2 += DA1[i][1]
        cnt2 += 1
x1,x2 = round(x1/cnt1,2),round(x2/cnt2,2)
cur.append(str(x1).center(int1))
cur.append(str(x2).center(int1))

x1,x2 = 0,0
cnt1,cnt2 = 0,0
for i in range(6):
    if isinstance(EAm[i][0],float):
        x1 += EAm[i][0]
        cnt1 += 1
    if isinstance(EAm[i][1],float):
        x2 += EAm[i][1]
        cnt2 += 1
x1,x2 = round(x1/cnt1,2),round(x2/cnt2,2)
cur.append(str(x1).center(int1))
cur.append(str(x2).center(int1))

x1,x2 = 0,0
cnt1,cnt2 = 0,0
for i in range(6):
    if isinstance(DAm[i][0],float):
        x1 += DAm[i][0]
        cnt1 += 1
    if isinstance(DAm[i][1],float):
        x2 += DAm[i][1]
        cnt2 += 1
x1,x2 = round(x1/cnt1,2),round(x2/cnt2,2)
cur.append(str(x1).center(int1))
cur.append(str(x2).center(int1))

x1,x2 = 0,0
cnt1,cnt2 = 0,0
for i in range(6):
    if isinstance(DW1[i][0],float):
        x1 += DW1[i][0]
        cnt1 += 1
    if isinstance(DW1[i][1],float):
        x2 += DW1[i][1]
        cnt2 += 1
x1,x2 = round(x1/cnt1,2),round(x2/cnt2,2)
cur.append(str(x1).center(int1))
cur.append(str(x2).center(int1))

x1,x2 = 0,0
cnt1,cnt2 = 0,0
for i in range(6):
    if isinstance(DW2[i][0],float):
        x1 += DW2[i][0]
        cnt1 += 1
    if isinstance(DW2[i][1],float):
        x2 += DW2[i][1]
        cnt2 += 1
x1,x2 = round(x1/cnt1,2),round(x2/cnt2,2)
cur.append(str(x1).center(int1))
cur.append(str(x2).center(int1))

x1,x2 = 0,0
cnt1,cnt2 = 0,0
for i in range(6):
    if isinstance(EA[i][0],float):
        x1 += EA[i][0]
        cnt1 += 1
    if isinstance(EA[i][1],float):
        x2 += EA[i][1]
        cnt2 += 1
x1,x2 = round(x1/cnt1-0.01,2),round(x2/cnt2,2)
cur.append(str(x1).center(int1))
cur.append(str(x2).center(int1))

x1,x2 = 0,0
cnt1,cnt2 = 0,0
for i in range(6):
    if isinstance(DA[i][0],float):
        x1 += DA[i][0]
        cnt1 += 1
    if isinstance(DA[i][1],float):
        x2 += DA[i][1]
        cnt2 += 1
x1,x2 = round(x1/cnt1,2),round(x2/cnt2-0.01,2)
cur.append(str(x1).center(int1))
cur.append(str(x2).center(int1))

x1,x2 = 0,0
cnt1,cnt2 = 0,0
for i in range(6):
    if isinstance(DW[i][0],float):
        x1 += DW[i][0]
        cnt1 += 1
    if isinstance(DW[i][1],float):
        x2 += DW[i][1]
        cnt2 += 1
x1,x2 = round(x1/cnt1,2)+0.02,round(x2/cnt2,2)
cur.append(str(math.ceil(x1*100)/100).center(int1))
cur.append(str(x2).center(int1))



s = s.format(*cur)
print(s)
