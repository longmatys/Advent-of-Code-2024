import re
print(1)
def test_run(run,prohibits):
    fail = {'sets':set(),'appears':{}}
    
    for i,dig in enumerate(run):
        if dig in fail['sets']:
            print(run,dig,fail['appears'])
            return (fail['appears'].get(dig),i)
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
    for run in runs:
        res = test_run(run,prohibits)
        print('zde',res)
        if res is None:
            continue
        while res:=test_run(run,prohibits):
            #print(res)
            run = swap(run,res)
        print(run)
def part1(runs,prohibits):
    
        
    print(sum([ run[int(len(run)/2)] for run in runs if test_run(run,prohibits)==None]))
        
def go():
    rules = []
    runs = []
    prohibits = {'sets':{},'appears':{}}
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
                    proh_x = prohibits['sets'].get(rules[-1][1],set())
                    proh_x.add(rules[-1][0])
                    prohibits['sets'][rules[-1][1]] = proh_x
                    
            else:
                runs.append([int(part) for part in line.split(',')])
        
        part1(runs,prohibits)
        part2(runs,prohibits)
go()
