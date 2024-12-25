import os
import tqdm
import itertools


def work(lock):
    #print('\n'.join(lock),'\n')
    if lock[0][0] == '#':
        pre = 'lock'
        counter_char = '.'
    else:
        pre = 'key'
        counter_char = '#'
    res = []
    for col in range(len(lock[0])):
        res.append(sum([1 for row in range(len(lock)) if lock[row][col] == counter_char]) -1)
    pass
    #print(pre, res)
    return pre, res
def test_locks(data):
    counter = 0
    for l, k in itertools.product(data['lock'], data['key']):
        if all([ll >= kk for ll, kk in zip(l, k)]): counter+=1
    print('Part 1:', counter)
def main():
    # Get the name of the Python script

    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    data = {
        'key': [],
        'lock': []
    }
    with open(input_file) as f:
        lock = []
        for line in tqdm.tqdm(f.readlines()):
            line = line.strip()
            if line == '':
                t, d = work(lock)
                data[t].append(d)
                lock = []
            else:
                lock.append(line)
    t, d = work(lock)
    data[t].append(d)
    
    test_locks(data)
            
if __name__ == '__main__':
    main()