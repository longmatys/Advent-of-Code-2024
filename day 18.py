import os
import heapq

dirs = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]
MAXIMUM = 71
START = (0, 0)
END = (MAXIMUM-1, MAXIMUM-1)


def get_value_simple(map_v, point):
    if point[0] < 0 or point[1] < 0 or \
            point[0] >= len(map_v[0]) or point[1] >= len(map_v):
        return None
    return map_v[point[1]][point[0]]


def work(data):
    map_v = [['.' for _ in range(MAXIMUM)] for _ in range(MAXIMUM)]

    for i, (x, y) in enumerate(data):
        map_v[y][x] = '#'
        heap = [(0, START)]
        map_values = [[-1 for _ in range(MAXIMUM)] for _ in range(MAXIMUM)]
        cache = {}
        while (heap):

            value, point = heapq.heappop(heap)
            cache[point] = None
            place = get_value_simple(map_v, point)
            if not place or place == '#':
                continue
            value_current = get_value_simple(map_values, point)
            if value_current is not None and \
                    value_current >= 0 and value_current < value:
                continue
            map_values[point[1]][point[0]] = value
            if point == END:
                continue
            for dir in dirs:
                value_new = \
                    get_value_simple(map_values,
                                     (point[0] + dir[0], point[1] + dir[1]))
                if value_new is not None and \
                        (value_new == -1 or value_new < value - 1):
                    value_cache = cache.get((point[0] + dir[0],
                                             point[1] + dir[1]), None)
                    if value_cache is None or value_cache > value + 1:
                        cache[(point[0] + dir[0],
                               point[1] + dir[1])] = value + 1
                        heapq.heappush(heap, (value + 1,
                                              (point[0] + dir[0],
                                               point[1] + dir[1])))

        print(f"End value {i}.fallen ({x, y}): ",
              map_values[MAXIMUM-1][MAXIMUM-1])
        if map_values[MAXIMUM-1][MAXIMUM-1] == -1:
            return


def main():
    # Get the name of the Python script

    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'

    with open(input_file) as f:
        data = [(int(term.split(',')[0]), int(term.split(',')[1]))
                for term in [line.strip() for line in f]]
        work(data)


if __name__ == '__main__':
    main()
