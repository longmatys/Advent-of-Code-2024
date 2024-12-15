import os
import logging
import tqdm
MODE_MAP = 1
MODE_INSTRUCTIONS = 2
SPACE_FREE = '.'
SPACE_WALL = '#'
SPACE_BOX = 'O'
SPACE_START = '['
SPACE_END = ']'
DIR_UP = (0,-1)
DIR_DOWN = (0,1)
dirs = {
    '^': DIR_UP,
    'v': DIR_DOWN,
    '<': (-1,0),
    '>': (1,0)
}
offset_double = {
    '[': 0,
    ']': -1
}
def get_value(map_v,point):
    if point[0] < 0 or point[1] < 0 or point[0] >= len(map_v[0]) or point[1] >= len(map_v) :
        return None
    return  map_v[point[1]][point[0]]
def move_to_part2_double(map_v,point,dir_v, move_data):
    value_dir = get_value(map_v,(point[0],point[1]+dir_v[1]))
    value_dir_right = get_value(map_v,(point[0]+1,point[1]+dir_v[1]))
    if point[0] < 0 or point[1] < 0 or point[0] >= len(map_v[0]) or point[1] >= len(map_v) or value_dir=='#' or value_dir_right=='#':
        return False   
    elif value_dir == SPACE_FREE and value_dir_right == SPACE_FREE:
        #if move_data:
        #    assert False, "TODO"            
        return True    
    elif value_dir == SPACE_START:                   
        res1 = move_to_part2_double(map_v,(point[0]+dir_v[0],point[1]+dir_v[1]),dir_v,move_data)
        if move_data:
            map_v[point[1]+2*dir_v[1]][point[0]+dir_v[0]] = map_v[point[1]+dir_v[1]][point[0]+dir_v[0]]
            map_v[point[1]+dir_v[1]][point[0]+dir_v[0]] = SPACE_FREE
            map_v[point[1]+2*dir_v[1]][point[0]+dir_v[0]+1] = map_v[point[1]+dir_v[1]][point[0]+dir_v[0]+1]
            map_v[point[1]+dir_v[1]][point[0]+dir_v[0]+1] = SPACE_FREE
        return res1
    elif value_dir == SPACE_END:
        res1 = move_to_part2_double(map_v,(point[0]+dir_v[0]-1,point[1]+dir_v[1]),dir_v,move_data)
        if move_data:
            map_v[point[1]+2*dir_v[1]][point[0]+dir_v[0]] = map_v[point[1]+dir_v[1]][point[0]+dir_v[0]]
            map_v[point[1]+dir_v[1]][point[0]+dir_v[0]] = SPACE_FREE
            map_v[point[1]+2*dir_v[1]][point[0]+dir_v[0]-1] = map_v[point[1]+dir_v[1]][point[0]+dir_v[0]-1]
            map_v[point[1]+dir_v[1]][point[0]+dir_v[0]-1] = SPACE_FREE
        res2 = True
        if value_dir_right == SPACE_START:
            res2 = move_to_part2_double(map_v,(point[0]+dir_v[0]+1,point[1]+dir_v[1]),dir_v,move_data)
            if move_data:                
                map_v[point[1]+2*dir_v[1]][point[0]+dir_v[0]+1] = map_v[point[1]+dir_v[1]][point[0]+dir_v[0]+1]
                map_v[point[1]+dir_v[1]][point[0]+dir_v[0]+1] = SPACE_FREE
                map_v[point[1]+2*dir_v[1]][point[0]+dir_v[0]+2] = map_v[point[1]+dir_v[1]][point[0]+dir_v[0]+2]
                map_v[point[1]+dir_v[1]][point[0]+dir_v[0]+2] = SPACE_FREE
        return res1 and res2
    else:
        res2 = move_to_part2_double(map_v,(point[0]+dir_v[0]+1,point[1]+dir_v[1]),dir_v,move_data)
        if move_data:
            map_v[point[1]+2*dir_v[1]][point[0]+dir_v[0]+1] = map_v[point[1]+dir_v[1]][point[0]+dir_v[0]+1]
            map_v[point[1]+dir_v[1]][point[0]+dir_v[0]+1] = SPACE_FREE
            map_v[point[1]+2*dir_v[1]][point[0]+dir_v[0]+2] = map_v[point[1]+dir_v[1]][point[0]+dir_v[0]+2]
            map_v[point[1]+dir_v[1]][point[0]+dir_v[0]+2] = SPACE_FREE
        return res2
    assert False, "Unpredicted"
def move_to_part2(map_v,point,dir_v):
    if point[0] < 0 or point[1] < 0 or point[0] >= len(map_v[0]) or point[1] >= len(map_v) or map_v[point[1]][point[0]] == SPACE_WALL:
        return False
    if map_v[point[1]][point[0]] == SPACE_FREE:
        return True
    value_down = get_value(map_v,(point[0],point[1]+1))
    value_up = get_value(map_v,(point[0],point[1]-1))
    if dir_v == DIR_UP and value_up == SPACE_START or dir_v == DIR_DOWN  and value_down == SPACE_START:        
        if move_to_part2_double(map_v, (point[0]+dir_v[0],point[1]+dir_v[1]),dir_v,False):
            move_to_part2_double(map_v, (point[0]+dir_v[0],point[1]+dir_v[1]),dir_v,True)
            map_v[point[1]+2*dir_v[1]][point[0]+dir_v[0]] = map_v[point[1]+dir_v[1]][point[0]+dir_v[0]]
            map_v[point[1]+dir_v[1]][point[0]+dir_v[0]] = SPACE_FREE
            map_v[point[1]+2*dir_v[1]][point[0]+dir_v[0]+1] = map_v[point[1]+dir_v[1]][point[0]+dir_v[0]+1]
            map_v[point[1]+dir_v[1]][point[0]+dir_v[0]+1] = SPACE_FREE
            
            map_v[point[1]+dir_v[1]][point[0]+dir_v[0]] = map_v[point[1]][point[0]]
            map_v[point[1]][point[0]] = SPACE_FREE
            return True
        else:
            return False
    elif dir_v == DIR_UP and value_up == SPACE_END or dir_v == DIR_DOWN  and value_down == SPACE_END:
        if move_to_part2_double(map_v, (point[0]+dir_v[0]-1,point[1]+dir_v[1]),dir_v,False):
            move_to_part2_double(map_v, (point[0]+dir_v[0]-1,point[1]+dir_v[1]),dir_v,True)
            map_v[point[1]+2*dir_v[1]][point[0]+dir_v[0]] = map_v[point[1]+dir_v[1]][point[0]+dir_v[0]]
            map_v[point[1]+dir_v[1]][point[0]+dir_v[0]] = SPACE_FREE
            map_v[point[1]+2*dir_v[1]][point[0]+dir_v[0]-1] = map_v[point[1]+dir_v[1]][point[0]+dir_v[0]-1]
            map_v[point[1]+dir_v[1]][point[0]+dir_v[0]-1] = SPACE_FREE
            
            map_v[point[1]+dir_v[1]][point[0]+dir_v[0]] = map_v[point[1]][point[0]]
            map_v[point[1]][point[0]] = SPACE_FREE
            return True
        else:
            return False
    elif move_to_part2(map_v,(point[0]+dir_v[0],point[1]+dir_v[1]),dir_v):
        map_v[point[1]+dir_v[1]][point[0]+dir_v[0]] = map_v[point[1]][point[0]]
        map_v[point[1]][point[0]] = SPACE_FREE
        return True
    else:
        return False
def move_to(map_v,point,dir_v):
    if point[0] < 0 or point[1] < 0 or point[0] >= len(map_v[0]) or point[1] >= len(map_v) or map_v[point[1]][point[0]] == SPACE_WALL:
        return False
    if map_v[point[1]][point[0]] == SPACE_FREE:
        return True
    if move_to(map_v,(point[0]+dir_v[0],point[1]+dir_v[1]),dir_v):
        map_v[point[1]+dir_v[1]][point[0]+dir_v[0]] = map_v[point[1]][point[0]]
        map_v[point[1]][point[0]] = SPACE_FREE
        return True
    else:
        return False
def expand_map(map_v):
    result = []
    for line in map_v:
        line_new = []
        for piece in line:
            if piece in ['#','.']:
                line_new+= piece * 2
            elif piece == 'O':
                line_new+=['[',']']
            elif piece == '@':
                line_new+=['@','.']
        result.append(line_new)
    return result
def process(map_v,instructions_v):
    
    map_v_expanded = expand_map(map_v)
    point1 = [[x_i,y_i] for y_i,y in enumerate(map_v) for x_i,x in enumerate(y) if x=='@'][0]
    point2 = [[x_i,y_i] for y_i,y in enumerate(map_v_expanded) for x_i,x in enumerate(y) if x=='@'][0]
    for instr in tqdm.tqdm(instructions_v):
        if move_to_part2(map_v_expanded,point2,dirs[instr]):
            point2[0]=point2[0]+dirs[instr][0]
            point2[1]=point2[1]+dirs[instr][1]
        if move_to(map_v,point1,dirs[instr]):
            point1[0]=point1[0]+dirs[instr][0]
            point1[1]=point1[1]+dirs[instr][1]
    
    res1 = sum([(y_i+1)*100+(x_i+1) for y_i,y in enumerate(map_v) for x_i,x in enumerate(y) if x==SPACE_BOX])
    res2 = sum([(y_i+1)*100+(x_i+2) for y_i,y in enumerate(map_v_expanded) for x_i,x in enumerate(y) if x==SPACE_START])
    print('Part 1:', res1)
    print('Part 2:', res2)
    
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    map_v=[]
    instructions=[]
    mode = MODE_MAP
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '#':
                continue
            if line == '':
                mode=MODE_INSTRUCTIONS
                continue
            elif mode==MODE_MAP:
                map_v.append(list(line[1:-1]))
            else:
                instructions.append(line)
    process(map_v[1:-1],''.join(instructions))
if __name__ == '__main__':
    main()