    
import os
import json

pjPath = "/Users/yixuanyan/yyx/github/jarvis/Jarvis/ps"
gtPath = "/Users/yixuanyan/yyx/github/jarvis/Jarvis/ground_truth/macro_benchmark"
pjList = ['bpytop','furl','rich-cli','sqlparse','sshtunnel','TextRank4ZH']
entry_bpytop = ['bpytop']

entry_sshtunnel = ['sshtunnel']


entry_rich_cli = ['rich_cli.__main__','rich_cli.markdown', 'rich_cli.pager', 'rich_cli.win_vt','rich_cli.markdown.CodeBlock', 'rich_cli']

entry_sqlparse = ['sqlparse.filters.reindent',
                  'sqlparse.filters.right_margin',
                  'sqlparse.filters.__init__',
                  'sqlparse.filters.tokens',
                  'sqlparse.filters.aligned_indent',
                  'sqlparse.filters.others',
                  'sqlparse.filters.output',
                  'sqlparse.formatter',
                  'sqlparse.keywords',
                  'sqlparse.__init__',
                  'sqlparse.tokens',
                  'sqlparse.cli',
                  'sqlparse.utils',
                  'sqlparse.lexer',
                  'sqlparse.exceptions',
                  'sqlparse.sql',
                  'sqlparse.engine.filter_stack',
                  'sqlparse.engine.grouping',
                  'sqlparse.engine.__init__',
                  'sqlparse/.engine.statement_splitter',
                  'sqlparse.__main__',
                  "sqlparse.cli.main",
                  "sqlparse.cli.create_parser",
                  "sqlparse.format",
                  "sqlparse.parse",
                  "sqlparse.lexer.tokenize",
                  "sqlparse.utils.remove_quotes"
                  ]

entry_text = ['textrank4zh', 
              'textrank4zh.Segmentation', 
              'textrank4zh.TextRank4Keywordn', 
              'textrank4zh.TextRank4Sentence',
              'textrank4zh.util',
              "textrank4zh.Segmentation.Segmentation.__init__",
              "textrank4zh.Segmentation.Segmentation.segment",
              "textrank4zh.TextRank4Keyword.TextRank4Keyword.__init__","textrank4zh.TextRank4Keyword.TextRank4Keyword.analyze","textrank4zh.TextRank4Sentence.TextRank4Sentence.__init__","textrank4zh.TextRank4Sentence.TextRank4Sentence.analyze"
              ]

entry_furl = ['furl.furl',  
              'furl.furl.Fragment.__repr__',
              'furl.furl.furl.__repr__',
              'furl.furl.furl.__truediv__',
              'furl.furl.Path.__eq__',
              'furl.furl.Path.__truediv__',
              'furl.furl.Query.__eq__',
              'furl.furl.Query.__repr__',
              'furl.furl.Query.params',
              'furl.furl.QueryCompositionInterface.querystr'
              'furl.common', 
              'furl.compat', 
              'furl.furl.Fragment.__bool__',
              'furl.furl.Fragment.__eq__',
              'furl.furl.FragmentCompositionInterface.fragmentstr',
              'furl.furl.furl.asdict',
              'furl.furl.furl.join',
              'furl.furl.furl.remove',
              'furl.furl.Path.__repr__',
              'furl.furl.Path.normalize',
              'furl.furl.Path.set',
              'furl.furl.PathCompositionInterface.pathstr',
              'furl.furl.Query.__bool__',
              'furl.furl.QueryCompositionInterface.args',
              'furl.omdict1D.omdict1D.__setitem__',
              'furl.omdict1D',
              'furl',
              "furl.omdict1D.omdict1D.add"
              "furl.omdict1D.omdict1D.set",
              ]



def convert_EA(pj):
    
    pj_input = os.path.join(pjPath,pj,'EA.json')
    pj_output = os.path.join(pjPath,pj,'EA_final.json')
    with open(pj_input,'r') as f:
        pj_data = json.load(f)
    nodes = {}
    edges = {}
    for x,y in pj_data['graph']['nodes'].items():
        nodes[x] = y['name'].replace('::', '.').replace('.(global)', '')
    for item in pj_data['graph']['edges']:
        edges[item['source']] = item['target']
    # print(nodes)
    # print(edges)
    data = {}
    for x,y in edges.items():
        data.setdefault(nodes[x],[])
        data[nodes[x]].append(nodes[y])
    with open(pj_output,'w') as f:
        json.dump(data,f)
        
pjList = ['bpytop','furl','rich-cli','sqlparse','sshtunnel','TextRank4ZH']
def convert_EW(pj):
    pj_input = os.path.join(pjPath,pj,'EW.json')
    pj_output = os.path.join(pjPath,pj,'EW_final.json')
    with open(pj_input,'r') as f:
        pj_data = json.load(f)
    nodes = {}
    edges = {}
    for x,y in pj_data['graph']['nodes'].items():
        nodes[x] = y['name'].replace('::', '.').replace('.(global)', '')
    for item in pj_data['graph']['edges']:
        edges[item['source']] = item['target']
    # print(nodes)
    # print(edges)
    data = {}
    for x,y in edges.items():
        data.setdefault(nodes[x],[])
        data[nodes[x]].append(nodes[y])
    with open(pj_output,'w') as f:
        json.dump(data,f)
        
def E2D(pj,startList):
    pj_input_ea = os.path.join(pjPath,pj,'EA_final.json')
    pj_output_da = os.path.join(pjPath,pj,'DA.json')
    pj_input_ew = os.path.join(pjPath,pj,'EW_final.json')
    pj_output_dw = os.path.join(pjPath,pj,'DW.json')
    
    with open(pj_input_ea,'r') as f:
        ea_data = json.load(f)
    tmpJson = {}
    visited = set()
    entryList = []
    for entry in ea_data.keys():
        for start in startList:
            if start.endswith(entry):
                entryList.append(entry)
    # entryList = startList[:]
    
    while entryList:
        entry = entryList[0]
        visited.add(entry)
        entryList.remove(entry)
        tmpJson[entry] = []
        if entry not in ea_data:
            continue
        for v in ea_data[entry]:
            tmpJson[entry].append(v)
            if v not in visited:
                entryList.append(v)
    with open(pj_output_da,'w') as f:
        json.dump(tmpJson,f)
    if not os.path.exists(pj_input_ew):
        return
    with open(pj_input_ew,'r') as f:
        ew_data = json.load(f)
    
    tmpJson = {}
    visited = set()
    entryList = []
    for entry in ew_data.keys():
        for start in startList:
            if start.endswith(entry):
                entryList.append(entry)
    # entryList = startList[:]
    print(entryList)
    while entryList:
        entry = entryList[0]
        visited.add(entry)
        entryList.remove(entry)
        tmpJson[entry] = []
        if entry not in ew_data:
            continue
        for v in ew_data[entry]:
            tmpJson[entry].append(v)
            if v not in visited:
                entryList.append(v)
    with open(pj_output_dw,'w') as f:
        json.dump(tmpJson,f)
# for pj in pjList:
#     convert_EA(pj)
#     try:
#         convert_EW(pj)
#     except:
#         print(pj+' has no EW.json')
# E2D('bpytop',entry_bpytop)
# E2D('sshtunnel',entry_sshtunnel)
# E2D('rich-cli',entry_rich_cli)
# E2D('sqlparse',entry_sqlparse)
# E2D('furl',entry_furl)
# E2D('TextRank4ZH',entry_text)

def result(pj):
    with open(os.path.join(gtPath,pj,'DA.json'),'r') as f:
        da_gt = json.load(f)
    with open(os.path.join(pjPath,pj,'DA.json'),'r') as f:
        da_data = json.load(f)
    gt_total = 0
    da_total = 0
    TP = 0
    for t1 in da_gt:
        gt_total += len(da_gt[t1])
    for t2 in da_data:
        da_total += len(da_data[t2])
    for t1 in da_gt:
        for t2 in da_data:
            if t1.endswith(t2):
                for gt_entry in da_gt[t1]:
                    for da_entry in da_data[t2]:
                        if gt_entry.endswith(da_entry):
                            TP += 1
    print(pj,":" ,"DA precision: ",TP/da_total,"DA recall: ",TP/gt_total)

    pass

    with open(os.path.join(gtPath,pj,'EA.json'),'r') as f:
        ea_gt = json.load(f)
    with open(os.path.join(pjPath,pj,'EA_final.json'),'r') as f:
        ea_data = json.load(f)
    gt_total = 0
    ea_total = 0
    TP = 0
    for t1 in ea_gt:
        gt_total += len(ea_gt[t1])
    for t2 in ea_data:
        ea_total += len(ea_data[t2])
    for t1 in ea_gt:
        for t2 in ea_data:
            if t1.endswith(t2):
                for gt_entry in ea_gt[t1]:
                    for ea_entry in ea_data[t2]:
                        if gt_entry.endswith(ea_entry):
                            TP += 1
    print(pj,":" ,"EA precision: ",TP/ea_total,"EA recall: ",TP/gt_total)
    
    
    with open(os.path.join(gtPath,pj,'EA.json'),'r') as f:
        dw_gt = json.load(f)
    if not os.path.exists(os.path.join(pjPath,pj,'DW.json')):
        return
    with open(os.path.join(pjPath,pj,'DW.json'),'r') as f:
        dw_data = json.load(f)
    gt_total = 0
    dw_total = 0
    TP = 0
    for t1 in dw_gt:
        gt_total += len(dw_gt[t1])
    for t2 in dw_data:
        dw_total += len(dw_data[t2])
    for t1 in dw_gt:
        for t2 in dw_data:
            if t1.endswith(t2):
                for gt_entry in dw_gt[t1]:
                    for dw_entry in dw_data[t2]:
                        if gt_entry.endswith(dw_entry):
                            TP += 1
    print(pj,":" ,"DW precision: ",TP/dw_total,"DW recall: ",TP/gt_total)

    pass
for pj in pjList:
    result(pj)