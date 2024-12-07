import os
import logging
import tqdm
import operator
import concurrent.futures
def concatenate(a,b):
    return int(str(a) + str(b))
def try_ops(sum_v,operands,operators):
    if len(operands)==1:
        return [operands[0]]
    res_prev = try_ops(sum_v,operands[:-1],operators)
    res = []
    for op in operators:
        for res_prev_item in res_prev:
            if op(res_prev_item,operands[-1]) <= sum_v:
                res.append(op(res_prev_item,operands[-1]))
                
        
    return res
def part(data,operators):
    total_sum = 0
    for line in tqdm.tqdm(data):
        sum_v = int(line.split(':')[0])
        operands = [int(num) for num in line.split(':')[1].split()]
        res = try_ops(sum_v,operands,operators)
        if res.count(sum_v) > 0:
            total_sum+=sum_v
    return total_sum    
    
    
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    with open(input_file) as f:
        data = [line.strip() for line in f]
    res = part(data,[operator.mul, operator.add])
    print('Part 1:',res)
    res = part(data,[operator.mul, operator.add, concatenate])
    print('Part 2:',res)
if __name__ == '__main__':
    main()