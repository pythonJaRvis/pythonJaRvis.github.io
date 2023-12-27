import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
plt.rcParams["font.family"] = "Times New Roman"
import os
base = os.getcwd()
pjPath = ['bpytop','sqlparse','text','furl','rich-cli','sshtunnel']
memo = {}
for pj in pjPath:
    memo[pj] = []
    with open(os.path.join(base,'reproducing_RQ1','FAG','jarvis',pj+".txt"),'r') as f:
        lines = f.readlines()
        for line in lines:
            memo[pj].append(list(map(int,(line.strip().split(":")))))



def format_func(value, tick_number):
    return f"{value/1000:.0f}k" if value > 0 else 0

fig, axs = plt.subplots(2, 3)
for i in range(2):
    for j in range(3):
        index = 3 * i + j
        pj = pjPath[index]
        ax = axs[i, j]  
        x = list(map(lambda x:x[0],memo[pj]))
        y = list(map(lambda x:x[1],memo[pj]))
        ax.plot(x,y)
        ax.set_title(f'P{pjPath.index(pj)+1}') 
        ax.tick_params(labelsize=12)
        if index in [0,1,4]:
            ax.set_xticks(np.arange(0, max(x),step=max(x)//4))
            ax.xaxis.set_major_formatter(FuncFormatter(format_func))
            ax.yaxis.set_major_formatter(FuncFormatter(format_func))
        elif index == 2:
            ax.set_xticks(np.arange(0, max(x), 3000))
            ax.set_yticks([0,20000,40000,60000,70000])
            ax.xaxis.set_major_formatter(FuncFormatter(format_func))
            ax.yaxis.set_major_formatter(FuncFormatter(format_func))
        elif index == 5:
            ax.set_xticks(np.arange(0, max(x), step=max(x)//4))
            ax.set_yticks([0,10000,20000,30000,40000])
            ax.xaxis.set_major_formatter(FuncFormatter(format_func))
            ax.yaxis.set_major_formatter(FuncFormatter(format_func))
        elif index == 3:
            ax.set_xticks([0,900,1800,2700])
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x,tick_number:f'{round(x/1000,1)}k' if x > 0 else 0 ))
            ax.yaxis.set_major_formatter(FuncFormatter(format_func))
        ax.spines['top'].set_linewidth(1)  
        ax.spines['right'].set_linewidth(1) 
        ax.spines['bottom'].set_linewidth(1) 
        ax.spines['left'].set_linewidth(1)
#         ax.xticks(fontsize=24)
#         ax.yticks(fontsize=24)
plt.tight_layout()
# plt.show()
plt.savefig('./reproducing_RQ1/FAG/jarvis-fag.pdf')
plt.clf()


change = {}
change['bpytop'] = [[0,0,53377],
                    [41550,11827,14766],
                    [64104,4039,1262],
                    [68238,1167,2343],
                    [70938,810,5917],
                    [77219,446,4148],
                    [81491,322,1037],
                    [82718,132,81],
                    [82866,65,0],
                    [82869,62,0]
                   ]
change['furl'] = [[0,0,45168],
                  [35153,10015,10724],
                  [52422,3470,1131],
                  [56055,968,306],
                  [57038,291,225],
                  [57387,167,315],
                  [57691,178,48],
                  [57115,802,3395],
                  [59541,1771,1771],
                  [61804,1279,1029]
                 ]

change['rich-cli']=[[0,0,105012]]
change['sqlparse'] = [[0,0,45658],
                      [35626,10032,11371],
                      [53488,3541,1152],
                      [57313,868,600],
                      [58348,433,320],
                      [58973,128,83],
                      [59120,64,8],
                      [59157,35,0],
                      [59159,33,0],
                      [59158,34,0]
                     ]
change['sshtunnel'] = [[0,0,60400,],
                       [48645,11755,12879],
                       [69318,3961,1298],
                       [73540,1037,877],
                       [74878,576,578],
                       [75543,489,310],
                       [76049,293,74],
                       [76239,177,62],
                       [76354,124,60],
                       [76487,51,14],
                      ]
change['text'] = [[0,0,257200]]

# b---blue c---cyan g---green k----black
# m---magenta r---red w---white y----yellow
for pj, flag, c in zip(pjPath, ['o', 'v', '^', '*', 'x', 'd'], ['b', 'y', 'g', 'r', 'm', 'peru']):
    if pjPath.index(pj) == 2:
        x = [1]
        #         y = [257200]
        y = [99000]

        plt.plot(x, y, marker=flag, label=f'P{pjPath.index(pj) + 1}', markersize=5, color=c)
        continue
    if pjPath.index(pj) == 4:
        x = [1]
        y = [94012]
        plt.plot(x, y, marker=flag, label=f'P{pjPath.index(pj) + 1}', markersize=5, color=c)
        continue
    x = [i + 1 for i in range(len(change[pj]))]
    y = list(map(lambda x: x[0] + x[1] + x[2], change[pj]))
    #     plt.gca().set_xticks([1,2,3,4,5,6,7,8,9,10])
    plt.gca().set_xlim(0, 11)
    plt.gca().set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    plt.gca().set_xticklabels([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, '...'])

    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))
    plt.plot(x, y, label=f'P{pjPath.index(pj) + 1}', marker=flag, linewidth=0.5, markersize=5, color=c)
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)

plt.legend(loc='upper right', fontsize=14, frameon=False, ncol=2)
plt.yticks([45000, 50000, 60000, 70000, 80000, 90000, 92000, 95000, 97000, 100000],
           [r'45k', r'50k', r'60k', r'70k', r'80k', r'90k', '...', r'110k', '...', '260k'])

plt.xlabel("Number of iterations", fontsize=24)
plt.ylabel("AG Size (#)", fontsize=24)
# plt.show()
ax = plt.gca()
ax.spines['top'].set_linewidth(1)  # 顶部边框
ax.spines['right'].set_linewidth(1)  # 右侧边框
ax.spines['bottom'].set_linewidth(1)  # 底部边框
ax.spines['left'].set_linewidth(1)
plt.savefig('./reproducing_RQ1/FAG/pycg-ag.pdf', bbox_inches='tight')
plt.clf()

for pj, flag, c in zip(pjPath, ['o', 'v', '^', '*', 'x', 'd'], ['b', 'y', 'g', 'r', 'm', 'peru']):
    if pjPath.index(pj) == 2:
        x = [1]
        y = list(map(lambda x: (x[1] + x[2]) / (x[0] + x[1] + x[2]) * 100, change[pj]))
        plt.plot(x, y, marker=flag, label=f'P{pjPath.index(pj) + 1}', markersize=5)
        continue
    if pjPath.index(pj) == 4:
        x = [1]
        y = list(map(lambda x: (x[1] + x[2]) / (x[0] + x[1] + x[2]) * 100, change[pj]))
        plt.plot(x, y, marker=flag, label=f'P{pjPath.index(pj) + 1}', markersize=5)
        continue
    x = [i + 1 for i in range(len(change[pj]))]
    y = list(map(lambda x: (x[1] + x[2]) / (x[0] + x[1] + x[2]) * 100, change[pj]))

    #     plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))
    plt.plot(x, y, label=f'P{pjPath.index(pj) + 1}', marker=flag, linewidth=0.5, markersize=5, color=c)
    x = [i + 1 for i in range(len(change[pj]))]
    y = list(map(lambda x: (x[1] + x[2]) / (x[0] + x[1] + x[2]) * 100, change[pj]))
    plt.gca().set_xlim(0, 11)
    plt.gca().set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    plt.gca().set_xticklabels([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, '...'])
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    plt.plot(x, y)
plt.legend(loc='upper right', fontsize=14, frameon=False, ncol=2)
plt.xlabel("Number of iterations", fontsize=24)
plt.ylabel("AG Size Changed (%)", fontsize=24)
ax = plt.gca()
ax.spines['top'].set_linewidth(1) 
ax.spines['right'].set_linewidth(1) 
ax.spines['bottom'].set_linewidth(1) 
ax.spines['left'].set_linewidth(1)
# plt.show()
plt.savefig("./reproducing_RQ1/FAG/pycg-change-ag.pdf", bbox_inches='tight')