import os
import math
import tqdm


def mangle(secret):
    # Multiply
    t = secret * 64
    # mix
    secret ^= t
    # prune
    secret = secret % 16777216
    # divide
    t = math.floor(secret / 32)
    # mix
    secret ^= t
    # prune
    secret = secret % 16777216
    # multiply
    t = secret * 2048
    # mix
    secret ^= t
    # prune
    secret = secret % 16777216
    return secret


def work(secret):
    for _ in range(2000):
        secret = mangle(secret)
    return secret

values = {}
def work2(secret):
    last = [0] * 2001
    last[0] = secret % 10
    cache = []
    for i in range(1, 2001):
        secret = mangle(secret)
        monkey = secret % 10
        last[i] = monkey
    diffs = [b - a for a, b in zip(last, last[1:])]
    for i in range(4, 2001):
        if diffs[i - 4:i] in cache:
            continue
        cache.append(diffs[i - 4:i])
        values[tuple(diffs[i - 4:i])] = values.get(tuple(diffs[i - 4:i]), 0) + last[i]
    return secret


def main():
    # Get the name of the Python script

    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    result = 0
    with open(input_file) as f:
        
        for line in tqdm.tqdm(f.readlines()):
            line = line.strip()
            if line == '#':
                break
            result += work(int(line))
            work2(int(line))
    best = max(values, key=values.get)
    print('Part 1:', result)
    print('Part 2:', values[best])


if __name__ == '__main__':
    main()
