import os
import logging
import itertools
def valid_coord(point,max_x,max_y):
    if max_x and max_y:
        return point[0]>=0 and point[1]>=0 and point[0]<max_x and point[1]<max_y
    return True
def coord_iterator(start, step, max_x, max_y, num_points=None):
    """
    Iterator for coordinates (x, y).
    
    :param start: Tuple (a, b) representing the starting point.
    :param step: Tuple (I, J) representing the step size in x and y.    
    :param num_points: Number of points to generate (optional, infinite and self if None).
    :yield: Next coordinate (x, y).
    """
    x, y = start
    dx, dy = step
    
    counter = 0
    while True:
        if (num_points and num_points==1 and counter>0) or not num_points:
            candidate = (x+counter*dx, y+counter*dy)
            if valid_coord(candidate,max_x,max_y):
                yield candidate
            else:
                break
            if num_points is not None:
                num_points -= 1
                if num_points <= 0:
                    break
            
        
        counter+=1
        
        


def produce_antinodes(a,b,rows=None,columns=None,num_points=None):
    distance = get_distance(a,b)
    ret = {
        (a[0]+distance[0], a[1]+distance[1]),
        (b[0]-distance[0], b[1]-distance[1])
    }
    ret = set(coord_iterator(a,get_distance(a,b),columns,rows,num_points))
    ret.update(set(coord_iterator(b,get_distance(b,a),columns,rows,num_points)))
    
    return ret
def get_distance(a,b):
    return (a[0]-b[0],a[1]-b[1])
def create_analysis(data):
    analysis = {}
    for row_i,row in enumerate(data):
        for col_j,col in enumerate(row):
            if col == '.':
                continue
            d = analysis.get(col,[])
            d.append((col_j,row_i))
            analysis[col] = d
    return analysis

def part(data,num_points):
    analysis = create_analysis(data)
    result = set()
    for char in analysis.keys():        
        for (a,b) in itertools.combinations(analysis[char], 2):
            result.update( produce_antinodes(a,b,columns=len(data[0]),rows=len(data),num_points=num_points))
    
    return len(result)
def main():
    
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    with open(input_file) as f:
        data = [line.strip() for line in f]
        res = part(data,1)
        print(f'Part 1: {res}')
        res = part(data,None)
        print(f'Part 2: {res}')
if __name__ == '__main__':
    main()