import os
import logging
from collections import Counter


def part2(data):
    
    c2 = Counter(data[1])
    suma = 0
    for num in data[0]:
        suma += num*c2[num]
        print(f'{num}, {c2[num]}')
    print(suma)
def part1(data):
    data[0].sort()
    data[1].sort()
    result = 0
    
    for i,v in enumerate(data[0]):
        result+=abs(v-data[1][i])
        print(f'{i}:{v},{data[1][i]},{result}')
                
    #print(data)
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    data = [[],[]]
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '#':
                break
            line_data = line.split()
            for i in [0,1]:
                data[i].append(int(line_data[i]))
    
    #part1(data)
    part2(data)
if __name__ == '__main__':
    main()