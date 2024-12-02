import os
import logging
def test_line(line):
    candidate =True
    direction = None
    for i in range(len(line)-1):
        diff = line[i]-line[i+1]
        if abs(diff) < 1 or abs(diff) > 3:
            candidate = False
            break
        else:
            direction_local = 'up' if diff > 0 else 'down'                    
            if direction==None or direction==direction_local:
                    direction=direction_local
            else:
                candidate = False
                break
    if candidate:
        return (True,None)
    return (False,i)
def part1(data):
    counter = 0
    for line in data:
        (valid,bad) = test_line(line)
        counter+= 1 if valid else 0
        
    return counter
def part2(data):
    counter = 0
    for line in data:
        (valid,bad) = test_line(line)
        if not valid:
            for corr in [-1,0,1]:
                (valid,bad2) = test_line([line[x] for x in range(len(line)) if x!=(bad+corr)])
                
                if valid:
                    break
        counter+= 1 if valid else 0
        
    return counter
    ""
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    print('Results')
    with open(input_file) as f:
        data = []
        for line in f.readlines():
            if line == '#':
                break
            line = list(map(int,line.split()))
            data.append(line)
        res = part1(data)
        print(res)
        res = part2(data)
        print(res)
if __name__ == '__main__':
    main()