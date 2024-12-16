import os
import logging
import heapq

def get_value(map_v,point,dir_v):
    if point[0] < 0 or point[1] < 0 or point[0] >= len(map_v[0]) or point[1] >= len(map_v) :
        return None
    return  map_v[point[1]][point[0]].get(dir_v,None)
def get_value_simple(map_v,point):
    if point[0] < 0 or point[1] < 0 or point[0] >= len(map_v[0]) or point[1] >= len(map_v) :
        return None
    return  map_v[point[1]][point[0]]

def work(map_v):
    map_values = [ [dict() for _ in y] for y in map_v ]
    point = tuple([[x_i,y_i] for y_i,y in enumerate(map_v) for x_i,x in enumerate(y) if x=='S'][0])
    dir_v = (1,0)
    heap = [(0,point,dir_v,[])]
    total_result = set()
    best_score = None
    
    while(heap):
        (score,point,dir_v,point_path) = heapq.heappop(heap) 
        place=get_value_simple(map_v,point)
        if place == '#':
            continue
        if place == 'E':
            if best_score and best_score<len(point_path+[point]):
                break
            best_score = len(point_path+[point])
            total_result.update(point_path+[point])
            
            #break
            continue
        place_score = get_value(map_values,point,dir_v)
        if place_score and place_score < score:
            #I can get here with less score
            continue
        map_values[point[1]][point[0]][dir_v] = score
        #Same direction candidate
        heapq.heappush(heap,(score+1,(point[0]+dir_v[0],point[1]+dir_v[1]),dir_v,point_path+[point]))
        #clock-wise candidate
        heapq.heappush(heap,(score+1001,(point[0]+dir_v[1],point[1]-dir_v[0]),(dir_v[1],-dir_v[0]),point_path+[point]))
        #counter clock-wise candidate
        heapq.heappush(heap,(score+1001,(point[0]-dir_v[1],point[1]+dir_v[0]),(-dir_v[1],dir_v[0]),point_path+[point]))
        
                    
    
    print(f'Found end with score: {score} and len {best_score}, len2: {len(total_result)}')
    print("Here")
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    map_v = []
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '#':
                break
            map_v.append(list(line))
    work(map_v)
if __name__ == '__main__':
    main()