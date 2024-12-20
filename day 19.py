import os
import heapq
import tqdm
from functools import cache

"""Day 19 of Advent of Code
"""

options_map = {}
def parse_options(options):
    for opt in options:
        opt_v = options_map.get(opt[0], [])
        opt_v.append(opt)
        options_map[opt[0]] = opt_v
    return options_map

@cache
def count_it(line, i):
    if i == 0:
        return 1
    res = 0
    if variants := options_map.get(line[-i]):
        for variant in variants:
            if line[-i:].startswith(variant):
                res += count_it(line, i - len(variant))
    return res
def work2(data):
    result = []
    for line in tqdm.tqdm(data):
        result.append(count_it(line, len(line)))
    return result

def work(data, options_map):
    print(options_map)
    result = []
    for line in tqdm.tqdm(data):
        heap = []
        heapq.heappush(heap, len(line))
        ret = 0
        while heap:
            item_i = heapq.heappop(heap)
            if item_i == 0:
                ret += 1
                continue
            if variants := options_map.get(line[-item_i]):
                for variant in variants:
                    if line[-item_i:].startswith(variant):
                        heapq.heappush(heap, item_i - len(variant))
            print(len(heap))
        print(ret,line)
        result.append(ret)
    return result


def main():
    # Get the name of the Python script
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    data = []
    with open(input_file, encoding="utf-8") as f:
        options = [opt.strip() for opt in f.readline().strip().split(',')]
        f.readline()
        for line in f.readlines():
            line = line.strip()
            if line == '#':
                break
            data.append(line)
    parse_options(options)
    result = work2(data)
    print('Part 1:', len([ x for x in result if x]))
    print('Part 2:', sum([ x for x in result if x]))


if __name__ == '__main__':
    main()
