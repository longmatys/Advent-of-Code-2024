import os
import logging
import copy
import tqdm
LAST_DIGIT = 9
dirs=[
    (1,0),
    (0,1),
    (-1,0),
    (0,-1)
]
def convert(znak):
    if znak == '.':
        return -1
    else:
        return int(znak)

def find_starts(data):
    return [(x_i,y_i) for y_i,y in enumerate(data) for x_i,x in enumerate(y) if x==0]
def walk_it(data,point,last_value):
    if point[0]<0 or point[1]<0 or point[0] >=len(data[0]) or point[1] >= len(data[1]) or last_value!=data[point[1]][point[0]]-1:
        return (set(),0)
    if data[point[1]][point[0]] == LAST_DIGIT:
        return (set([point]),1)
    res = set()
    res_count = 0
    for dir in dirs:
            (w_set,w_count) = walk_it(data,(point[0]+dir[0],point[1]+dir[1]),data[point[1]][point[0]])
            res.update(w_set)
            res_count+=w_count

    return (res,res_count)
def solve(data):
    
    total = 0
    res_count = 0
    for point in find_starts(data):
        res = set()
        for dir in dirs:
            (w_set,w_count) = walk_it(data,(point[0]+dir[0],point[1]+dir[1]),data[point[1]][point[0]])
            res.update(w_set)
            res_count+=w_count
        total+=len(res)

    return (total,res_count)
    
def part2(data):
    return 0
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    
    with open(input_file) as f:
        data = [list(map(convert,line.strip())) for line in f.readlines()]
        
    (p1,p2) = solve(data)
    print('Part 1:',p1)
    print('Part 2:', p2)
    
    
if __name__ == '__main__':
    main()