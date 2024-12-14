import os
import logging
import copy
import tqdm
import json

dirs=[
    (1,0),
    (0,1),
    (-1,0),
    (0,-1)
]
def get_parent(point,areas):
     d = areas[point]
     if d["parent"]:
        return get_parent(d["parent"],areas)
     return point
     
def get_neighbors(data,point):
    neighbors = []
    for dir in dirs:
            if point[1]+dir[1] < 0 or point[0]+dir[0] < 0 or point[1]+dir[1] >= len(data) or point[0]+dir[0] >= len(data[0]):
                 continue
            neighbors.append((point[0]+dir[0],point[1]+dir[1]))
    return neighbors
def reset_parent(areas,children_area,parent_point):
    for child in children_area["children"]:
        areas[child]["parent"] = parent_point
    children_area["parent"] = parent_point
DATA=0
AREA_ID = 1
PERIMETER = 2
def flood(map_data,point,area_id):
    map_data[point[1]][point[0]][AREA_ID]=area_id
    neighbors = get_neighbors(map_data,point)
    map_data[point[1]][point[0]][PERIMETER]=4
    
    for neighbor in neighbors:
        if map_data[point[1]][point[0]][DATA]==map_data[neighbor[1]][neighbor[0]][DATA]:
            map_data[point[1]][point[0]][PERIMETER]-=1
    for neighbor in neighbors:
        if map_data[point[1]][point[0]][DATA]==map_data[neighbor[1]][neighbor[0]][DATA] and map_data[neighbor[1]][neighbor[0]][AREA_ID]==-1:
            flood(map_data,neighbor,area_id)


def get_value(map_data,point,dir):
    if point[0]+dir[0]<0 or point[1]+dir[1]<0 or point[0]+dir[0]>=len(map_data[0]) or point[1]+dir[1]>=len(map_data):
        return -1
    return map_data[point[1]+dir[1]][point[0]+dir[0]][AREA_ID]

def count_it(map_data,cache):
    
    
    for y_i,y in enumerate(map_data):
        for x_i,x in enumerate(y):    
            value = get_value(map_data,(x_i,y_i),(0,0))
            value_left = get_value(map_data,(x_i,y_i),(-1,0))
            value_right = get_value(map_data,(x_i,y_i),(1,0))
            value_down = get_value(map_data,(x_i,y_i),(0,1))
            value_down_left = get_value(map_data,(x_i,y_i),(-1,1))
            value_down_right = get_value(map_data,(x_i,y_i),(1,1))
            if value != value_left:
                #there is fence up
                if value_down == -1 or \
                    value_down != value or \
                    value_down == value_down_left:
                    #yes, current upper line ends
                    cache[map_data[y_i][x_i][AREA_ID]][2]+=1
            if value != value_right:
                #there is fence up
                if value_down == -1 or \
                    value_down != value or \
                    value_down == value_down_right:
                    #yes, current bottom line ends
                    cache[map_data[y_i][x_i][AREA_ID]][2]+=1   
            
            value = get_value(map_data,(y_i,x_i),(0,0))
            value_up = get_value(map_data,(y_i,x_i),(0,-1))
            value_down = get_value(map_data,(y_i,x_i),(0,1))
            value_right = get_value(map_data,(y_i,x_i),(1,0))
            value_right_up = get_value(map_data,(y_i,x_i),(1,-1))
            value_right_down = get_value(map_data,(y_i,x_i),(1,1))
            if value != value_up:
                #there is fence up
                if value_right == -1 or \
                    value_right != value or \
                    value_right == value_right_up:
                    #yes, current upper line ends
                    cache[map_data[x_i][y_i][AREA_ID]][2]+=1
            if value != value_down:
                #there is fence up
                if value_right == -1 or \
                    value_right != value or \
                    value_right == value_right_down:
                    #yes, current bottom line ends
                    cache[map_data[x_i][y_i][AREA_ID]][2]+=1    
            
            cache[x[AREA_ID]][0]+=1
            cache[x[AREA_ID]][1]+=x[PERIMETER]
       
            
def work_v2(data):
    cache={}
    map_data = []
    for y_i,y in enumerate(data):
        map_data.append([])
        for x_i,x in enumerate(y):
            map_data[-1].append([x,-1,0])
    area_id = 0
    for y_i,y in enumerate(map_data):
        for x_i,x in enumerate(y):
            if x[AREA_ID]==-1:
                cache[area_id]=[0,0,0]
                flood(map_data,(x_i,y_i),area_id)
                area_id+=1
    count_it(map_data,cache)
    suma1 = sum([a*p for a,p,p2 in cache.values()])
    suma2 = sum([a*p2 for a,p,p2 in cache.values()])
    print("\nPart 1:",suma1,"\nPart 2:",suma2)

def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    
    with open(input_file) as f:
        data = [line.strip() for line in f]
        work_v2(data)
if __name__ == '__main__':
    main()