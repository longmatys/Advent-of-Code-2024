import os
import logging
import copy
import tqdm
POSITION_VALID = 0
POSITION_VISITED = 1
POSITION_INVALID =-1
def find_start_position(map_v):
    for y,line in enumerate(map_v):
        for x,char in enumerate(line):
            if char == '^':
                return (x,y)
    return None
def mark_position(visited,position,direction):
    if not position or not direction:
        return POSITION_INVALID
    pos = visited[position[1]][position[0]].get('dirs')
    if direction in pos:
        return POSITION_VISITED
    pos.append(direction)
    return POSITION_VALID
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
        elif field in ['#','O']:
            return (position,rotate_direction(direction))
        else:
            assert('NO WAY')

    return (None,None)

def dump_maps(map_v,visited):
    for y,line in enumerate(map_v):
        for x, char in enumerate(line):
            if len(visited[y][x]['dirs']) > 0:
                print('x',end='')
            else:
                print(char,end='')
        print('')
    print('')
def test_cycle(map_v,visited,position,direction):
    #map_v,visited,position,direction
    direction_rot = rotate_direction(direction)
    
    if direction_rot in visited[position[1]][position[0]]['dirs']:
        #Candidate for obstacle!
        if get_next_field(map_v,position,direction) in ['.','^']:
            #Test if obstacle can be placed
            (pos_new,dir_new) = move_position(map_v,position,direction)
            return pos_new
    return None


        
def part1(map_v,position,cycles,direction,visited,place_obstacle,maximum=None):
    if place_obstacle:
        progress_bar = tqdm.tqdm(total=maximum, desc="Progress")
    obstacles_tried = set()
    obstacles_valid = set()
    progress_last = 0
    while (res:=mark_position(visited,position,direction))==0:
        if place_obstacle:
            progress_current = sum([1 for line in visited for x in line if len(x['dirs'])>0])
            progress_bar.update(progress_current-progress_last)
            progress_last = progress_current
        #dump_maps(map_v,visited)
        if place_obstacle:
             #I want to place obstacles
             if get_next_field(map_v,position,direction) in ['.','^']:
                # There is free space to place obstacle
                (pos_new,dir_new) = move_position(map_v,position,direction)
                if pos_new not in obstacles_tried:  # Have not tried it already?
                    obstacles_tried.add(pos_new)    # Now I did!
                    #I havent tried it already
                    cache_position = copy.copy(position)
                    cache_cycles = copy.deepcopy(cycles)
                    cache_direction = rotate_direction(direction)
                    cache_visited = copy.deepcopy(visited)
                    #place obstacle and try it
                    map_v[pos_new[1]][pos_new[0]] = 'O' # Place obstacle
                    res = part1(map_v,cache_position,cache_cycles,cache_direction,cache_visited,False)
                    map_v[pos_new[1]][pos_new[0]] = '.' # Remove obstacle
                    if res[2] == POSITION_VISITED:
                        # It created a loop, so add it to the valid obstacle points
                        obstacles_valid.add(pos_new)
                #dump_maps(map_v,visited)           
                    


        #if position_cycle := test_cycle(map_v,visited,position,direction):
        #    cycles.add(position_cycle)
        (position,direction) = move_position(map_v,position,direction)
        ""
    #dump_maps(map_v,visited)
    if place_obstacle:
        progress_bar.close()
    return (sum([1 for line in visited for x in line if len(x['dirs'])>0]), len(obstacles_valid),res)
    

def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    
    with open(input_file) as f:
        map_v = [list(line.strip()) for line in f.readlines()]
        
    visited = [[{'dirs':[]} for _ in range(len(map_v))] for _ in range(len(map_v[0]))]
    visited2 = [[{'dirs':[]} for _ in range(len(map_v))] for _ in range(len(map_v[0]))]
    position = find_start_position(map_v)
    position2 = find_start_position(map_v)
    map_v[position[1]][position[0]] = '.'
    (p1,p2,res) = part1(map_v=map_v,position=position,cycles=set(),direction=(0,-1),visited=visited,place_obstacle=False)
    (p1,p2,res) = part1(map_v=map_v,position=position2,cycles=set(),direction=(0,-1),visited=visited2,place_obstacle=True,maximum=p1)
    print('Part 1:',p1)
    print('Part 2:', p2)
    print('Result:', res)
    
if __name__ == '__main__':
    main()