import os
import logging
def find_start_position(map_v):
    for y,line in enumerate(map_v):
        for x,char in enumerate(line):
            if char == '^':
                return (x,y)
    return None
def mark_position(visited,position,direction):
    if not position or not direction:
        return False
    pos = visited[position[1]][position[0]].get('dirs')
    if direction in pos:
        return False
    pos.append(direction)
    return True
def get_next_field(map_v,position,direction):
    new_x = position[0]+direction[0]
    new_y = position[1]+direction[1]
    if new_y >= len(map_v) or new_y < 0 or new_x >= len(map_v[0]) or new_x < 0:
        return None
    return map_v[new_y][new_x]
def rotate_direction(direction):
    if direction == (0,1):  # v
        direction = (-1,0)  # <
    elif direction == (-1,0):   # <
        direction = (0,-1)      # ^
    elif direction == (0,-1):   # ^
        direction = (1,0)       # >
    elif direction == (1,0):    # >
        direction = (0,1)       # v
    return direction
def move_position(map_v,position,direction):
    if field:=get_next_field(map_v,position,direction):
        if field in ['.','^']:
            return ((position[0]+direction[0],position[1]+direction[1]),direction)
        elif field == '#':
            return (position,rotate_direction(direction))
        else:
            assert('NO WAY')

    return (None,None)
def part2(map_v):
    ""
def dump_maps(map_v,visited):
    for y,line in enumerate(map_v):
        for x, char in enumerate(line):
            if len(visited[y][x]['dirs']) > 0:
                print('x',end='')
            else:
                print(char,end='')
        print('')
    print('')
def part1(map_v):
    position = find_start_position(map_v)
    
    direction = (0,-1)
    visited = [[{'dirs':[]} for _ in range(len(map_v))] for _ in range(len(map_v[0]))]
    while mark_position(visited,position,direction):
        #dump_maps(map_v,visited)
        (position,direction) = move_position(map_v,position,direction)
        ""
    print(sum([1 for line in visited for x in line if len(x['dirs'])>0]))
    #dump_maps(map_v,visited)
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    
    with open(input_file) as f:
        map_v = [line.strip() for line in f.readlines()]
        
    
    part1(map_v)
    part2(map_v)
if __name__ == '__main__':
    main()