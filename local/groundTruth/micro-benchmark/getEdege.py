import sys
import json

def main():
    pythoncg = sys.argv[1]
    pycg = sys.argv[2]
    pycg_cnt = process_file(pycg)
    pythoncg_cnt = process_file(pythoncg)
    output_path = sys.argv[3]
    ans = "pythonCG:\t{} \npycg1:\t{}".format(pythoncg_cnt,pycg_cnt)
    with open(output_path,'w') as f:
        f.write(ans)
def process_file(inputPath):
    with open(inputPath,'r') as f:
        fileJson = json.load(f)
    cnt =  get_count(fileJson)
    return cnt
    pass

def get_count(filejson:dict):
    cnt = 0
    for key in filejson:
        cnt += len(filejson[key])
    return cnt
if __name__ == '__main__':
    main()