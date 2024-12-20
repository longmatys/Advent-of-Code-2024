import os
import heapq
import tqdm
import copy
from line_profiler import LineProfiler


dirs = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


def get_value_simple(map_v, point, BORDER=1):
    if point[0] < 0 + BORDER or point[1] < 0 + BORDER or \
            point[0] + BORDER >= len(map_v[0]) or \
            point[1] + BORDER >= len(map_v):
        return None
    return map_v[point[1]][point[0]]


def find_shortest_path(map_v, point_start):
    map_values = [[-1 for _ in range(len(map_v[0]))]
                  for _ in range(len(map_v))]
    heap = [(0, point_start)]
    while heap:
        value, point = heapq.heappop(heap)
        place = get_value_simple(map_v, point)
        if not place or place == '#':
            continue
        value_current = get_value_simple(map_values, point)
        if value_current is not None and \
                value_current >= 0 and value_current < value:
            continue
        map_values[point[1]][point[0]] = value
        if place == 'E':
            return (value, map_values)

        for dir in dirs:
            value_new = \
                get_value_simple(map_values,
                                 (point[0] + dir[0], point[1] + dir[1]))
            if value_new is not None and \
                    (value_new == -1 or value_new < value - 1):
                heapq.heappush(heap, (value + 1,
                                      (point[0] + dir[0],
                                       point[1] + dir[1])))

def cheat(map_v, map_values, max_cheat):
    counter = 0
    for y in range(len(map_v)):
        for x in range(len(map_v[0])):
            if map_v[y][x] == '#': 
                continue
            for radius in range(2,max_cheat+1):
                for d_y in range (radius+1):
                    d_x = radius - d_y
                    for x_cand, y_cand in {(x + d_x, y + d_y), (x + d_x, y - d_y), (x - d_x, y + d_y), (x - d_x, y - d_y)}:
                        if x_cand < 0 or y_cand < 0 or x_cand >= len(map_v[0]) or y_cand >= len(map_v): 
                            continue
                        if map_v[y_cand][x_cand] == "#":
                            continue
                        if map_values[y][x] - map_values[y_cand][x_cand] >= 100 + radius:
                            counter += 1
    return counter
def work(map_v):
    
    point_start = tuple([[x_i, y_i] for y_i, y in enumerate(map_v)
                         for x_i, x in enumerate(y) if x == 'S'][0])
    

    (res_original, map_values) = find_shortest_path(map_v, point_start)
    counter = cheat(map_v, map_values, 2)
    print("Part 1: ", counter)
    counter = cheat(map_v, map_values, 20)
    print("Part 2: ", counter)
    


def main():
    # Get the name of the Python script
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    with open(input_file) as f:
        map_v = [list(line.strip()) for line in f.readlines()]
        work(map_v)


if __name__ == '__main__':
    main()
