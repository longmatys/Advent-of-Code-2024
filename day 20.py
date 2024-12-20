import os
import heapq
import tqdm
import copy


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


def work(map_v):
    SAVE = 50
    CHEAT_MAX = 20
    point_start = tuple([[x_i, y_i] for y_i, y in enumerate(map_v)
                         for x_i, x in enumerate(y) if x == 'S'][0])
    blocks = tuple([[x_i + 1, y_i + 1] for y_i, y in enumerate(map_v[1:-1])
                    for x_i, x in enumerate(y[1:-1]) if x != '#'])

    (res_original, map_values) = find_shortest_path(map_v, point_start)
    print(f'Part 1: {res_original}')
    shorts = set()
    for block in tqdm.tqdm(blocks):
        # Starting point for shortcuts
        value_orig = \
            get_value_simple(map_values, block)
        
        for dir in dirs:
            heap = []
            
            map_values_clone = copy.deepcopy(map_values)
            place = \
                get_value_simple(map_v,
                                 (block[0] + dir[0], block[1] + dir[1]),
                                 0)
            if place == '#':
                heapq.heappush(heap,(value_orig + 1,
                                     (block[0] + dir[0],
                                     block[1] + dir[1]),
                                     [block]))
            while heap:
                value, point, path = heapq.heappop(heap)
                place = get_value_simple(map_v, point)
                if not place or place == '#':
                    continue
                value_current = get_value_simple(map_values, point, 0)
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
    # saves = []
    # for block in tqdm.tqdm(blocks):
    #     map_v[block[1]][block[0]] = '.'
    #     (res, map_values) = find_shortest_path(map_v, point_start)
    #     if res != res_original:
    #         saves.append(res_original - res)
    #     map_v[block[1]][block[0]] = '#'
    # print(sorted([s for s in saves if s >= 100]))
    # print('Part 1', len([s for s in saves if s >= 100]))


def main():
    # Get the name of the Python script
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    with open(input_file) as f:
        map_v = [list(line.strip()) for line in f.readlines()]
        work(map_v)


if __name__ == '__main__':
    main()
