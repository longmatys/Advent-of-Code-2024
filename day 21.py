import os
from collections import deque
from itertools import product, chain
from functools import cache


KEYPAD1 = \
"""
789
456
123
X0A
"""
KEYPAD2 = \
"""
X^A
<v>
"""
DIRS = {
    
    'v': (0,1),
    '<': (-1,0),
    '^': (0,-1),
    '>': (1,0),
}


def analyze_keypad(keypad):
    result = {}
    for y_i, y in enumerate(keypad):
        for x_i, x in enumerate(y):
            if x == 'X':
                continue
            start = x
            result[start] = {start:[[]]}
            queue = deque([((x_i, y_i), [])])
            while queue:
                (qx, qy), path = queue.popleft()
                for ((dx, dy), dpath) in [((qx + t[0], qy + t[1]), path + [k]) for k, t in DIRS.items()]:
                    if dx < 0 or dy < 0 or dx >= len(keypad[0]) or dy >= len(keypad):
                        continue
                    if keypad[qy][qx] == 'X':
                        continue
                    if r := result[start].get(keypad[dy][dx]):
                        # path already exists is it shorter or the same?
                        if len(r[0]) < len(dpath):
                            # i already know a shorter path
                            continue
                        elif len(r[0]) == len(dpath):
                            # next candidate with same path distance
                            r.append(dpath)
                        else:
                            # i found a shorter way
                            result[start][keypad[dy][dx]] = [dpath]
                    else:
                        result[start][keypad[dy][dx]] = [dpath]
                    queue.append(((dx, dy), dpath))
    return result

def simulate(line, keypad, start):
    result = ""
    result_long = ""
    result_short = ""
    current_char = 'A'
    current = start
    #print(f'Analysing {line}')
    for x in line:
        if x == 'A':
            result_short += result[-1]
            result_long += f'\t O={result[-1]}\t'
            continue
        current_char = keypad[DIRS[x][1] + current[1]][DIRS[x][0] + current[0]]
        current = (DIRS[x][0] + current[0], DIRS[x][1] + current[1])
        result+=current_char
        result_long+=current_char

    return result_short
def gen_sequence(line, keypad):
    res = []
    current = 'A'

    for x in line:

        res.append(''.join(keypad[current][x]))
        current = x
    return 'A'.join(res)


def solve(line, keypad):
    ret = []
    for l1 in product(*[keypad[f][t] for f, t in zip('A' + line,line)]):
        ret.append('A'.join([''.join(sublist) for sublist in l1]) + 'A')
    return ret


def work(line):
    k_num = analyze_keypad(KEYPAD1.split())
    k_dir = analyze_keypad(KEYPAD2.split())
    robot1 = solve(line, k_num)
    next = robot1
    
    for _ in range(2):
        possible_next = []
        for seq in next:
            possible_next += solve(seq, k_dir)
        minlen = min(map(len, possible_next))
        next = [ seq for seq in possible_next if len(seq) == minlen]
    print(line, len(next[0]), int(line[:-1]), len(next))
    return len(next[0]) * int(line[:-1])
k_num = analyze_keypad(KEYPAD1.split())
k_dir = analyze_keypad(KEYPAD2.split())

@cache
def solve_bi(x, y, depth=2):
    if depth == 1:
        return len(k_dir[x][y][0]) + 1
    optimal = float("inf")
    for seq in [s + ["A"] for s in k_dir[x][y]]:
        length = 0
        for dx, dy in zip(['A'] + seq, seq):
            length += solve_bi(dx, dy, depth - 1)
        optimal = min(optimal, length)
    return optimal
          
def work_recursive(line):
    
    robot1 = solve(line, k_num)
    optimal = float("inf")
    for seq in robot1:
        length = 0
        for dx, dy in zip('A' + seq, seq):
            length += solve_bi(dx, dy, 25)
            pass
        optimal = min(optimal, length)
    print(robot1, optimal)
    return optimal * int(line[:-1])
    #res = [solve_bi(f, t, k_dir) for f, t in zip('A' + line,line)]
def main():
    # Get the name of the Python script
    
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    result = 0
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '#':
                break
            result += work_recursive(line)
        print('Part 1:',result)


if __name__ == '__main__':
    main()