import os
import logging
import re
def eval_mul(mul):
    res = re.findall(r'\d+',mul)
    return int(res[0])*int(res[1])
    
def part1(line):
    result = 0
    pattern=r'mul\(\d+,\d+\)'
    print(re.findall(pattern,line))
    for match in re.findall(pattern,line):
        result +=eval_mul(match)
    return result
def part2(line):
    result = 0
    pattern=r"mul\(\d+,\d+\)|do\(\)|don't\(\)"
    print(re.findall(pattern,line))
    do_enable = True
    for match in re.findall(pattern,line):
        if match=='do()':
            do_enable=True
        elif match=="don't()":
            do_enable=False
        elif do_enable:
            result +=eval_mul(match)
    return result
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    
    result_1=0
    result_2=0
    with open(input_file) as f:
        line = ' '.join(f.readlines())        
        result_1+=part1(line)
        result_2+=part2(line)
    print('Result 1:', result_1) 
    print('Result 2:', result_2)      
if __name__ == '__main__':
    main()