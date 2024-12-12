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
            if point[1]+dir[1] < 0 or point[0]+dir[0] < 0 or point[1]+dir[1] >= len(data) or point[1]+dir[1] >= len(data[0]):
                 continue
            neighbors.append((point[0]+dir[0],point[1]+dir[1]))
    return neighbors
def reset_parent(areas,children_area,parent_point):
    for child in children_area["children"]:
        areas[child]["parent"] = parent_point
    children_area["parent"] = parent_point
def work(data):
    areas = {}
    map_data = [[{"value":data[y_i][x_i], "domain":(y_i,x_i), "area":0, "perimeter":0}] for y_i,y in enumerate(data) for x_i,x in enumerate(y)]
    for y_i,line in enumerate(data):
        for x_i,el in enumerate(line):
            
            z = {"domain":(y_i,x_i), "area":1, "perimeter":4, "children":[], "parent":None}
            
            
            for neighbor in get_neighbors(data,(x_i,y_i)):
                same_value_neighbors = data[neighbor[1]][neighbor[0]] == el
                if same_value_neighbors:
                    #Same neighbor, so one fence less and one area more
                    z["perimeter"] -=1
                    
                if neighbor_area:=areas.get(neighbor):
                    #i am interested in only processed squares
                    if same_value_neighbors:
                        #they are the same
                        
                        parent_point = get_parent(neighbor,areas)
                        if parent_area := areas.get(parent_point):
                            #neighbor already has some area
                            if z["parent"]:
                                #i also have already a parent
                                areas[z["parent"]]["area"]+=parent_area["area"]
                                areas[z["parent"]]["fence"]+=parent_area["fence"]
                                areas[z["parent"]]["children"]+=parent_area["children"]+[parent_point]
                                reset_parent(areas,parent_area["children"],z["parent"])
                                
                            else:
                                #i dont have a parent, i will take this one
                                z["domain"] = neighbor_area["domain"]
                                z["parent"] = neighbor_area["parent"] if neighbor_area["parent"] else neighbor
                                z["perimeter"] += parent_area["perimeter"]
                                z["area"] += parent_area["area"]
                                parent_area["children"].append((y_i,x_i))
                        else:
                            #neighbor does not have parent
                            ""
                    else:
                        # Different value naighbors
                        ""
                else:
                    # Unprocessed squares
                    ""

                                

                    
                    
                print(x_i,y_i,el, neighbor)
            if z["parent"]:
                areas[z["parent"]]["area"] = z["area"]
                areas[z["parent"]]["perimeter"] = z["perimeter"]
                ""
            else:
                areas[(x_i,y_i)] = z
                
                
            
            

    print(map_data)
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    
    with open(input_file) as f:
        data = [line.strip() for line in f]
        work(data)
if __name__ == '__main__':
    main()