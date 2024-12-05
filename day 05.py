import re

def test_run(run,prohibits):
    #Return either None or tuple index of violating number indexes
    fail = {'sets':set(),'appears':{}}
    for i,dig in enumerate(run):        
        if dig in fail['sets']:
            x = run.index(prohibits['sets_straight'][dig].intersection(run[:i]).pop())
            return (x,i)
        if not fail['appears'].get(dig):
            fail['appears'][dig] = i 
        fail['sets'] = fail['sets'].union(prohibits['sets'].get(dig,set()))        
    return None
def swap(run,res):
    temp = run[res[0]]
    run[res[0]] = run[res[1]]
    run[res[1]] = temp
    return run
    ""
def part2(runs,prohibits):
    ret = 0
    for run in runs:
        res = test_run(run,prohibits)
        
        if res is None:
            continue
        while res:=test_run(run,prohibits):
            #print(res)
            run = swap(run,res)
        ret+=run[int(len(run)/2)]
    print('Part 2:',ret)
def part1(runs,prohibits):
    
        
    print('Part 1:',sum([ run[int(len(run)/2)] for run in runs if test_run(run,prohibits)==None]))
def update_set(set_v,k,v):
    proh_x = set_v.get(k,set())
    proh_x.add(v)
    set_v[k] = proh_x
def go():
    rules = []
    runs = []
    prohibits = {'sets':{},'sets_straight':{}}
    with open('day 05.input.txt') as f:
        phase=1
        for line in f.readlines():
            line = line.strip()
            if line == '':
                phase=2
                continue
            if phase==1:
                m = re.match(r"(\d+)\|(\d+)",line)
                if m:
                    
                    rules.append((int(m.group(1)),int(m.group(2))))
                    
                    
                    update_set(prohibits['sets'],rules[-1][1],rules[-1][0])
                    update_set(prohibits['sets_straight'],rules[-1][0],rules[-1][1])
                    
            else:
                runs.append([int(part) for part in line.split(',')])
        
        part1(runs,prohibits)
        part2(runs,prohibits)
go()
