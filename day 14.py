import os
import logging
import re
import math
import matplotlib.pyplot as plt
import numpy as np
import time
import tqdm

def get_destination(point,vector,size=(101,103),seconds=100):
    res=[(point[0]+vector[0]*seconds)%size[0], (point[1]+vector[1]*seconds)%size[1]]
    if res[0]<0:
        res[0]+=MAX_X
    if res[1]<0:
        res[1]+=MAX_Y
    
    return res
MAX_X=101
MAX_Y=103
# MAX_X=11
# MAX_Y=7
# 0,0  1,0
# 0,1  11

def calculate_image_entropy(array):
    # Flatten the 2D array to 1D
    flat_array = array.flatten()
    
    # Calculate the histogram (counts of unique values)
    unique, counts = np.unique(flat_array, return_counts=True)
    
    # Calculate probabilities
    probabilities = counts / counts.sum()
    
    # Calculate Shannon entropy
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy
def main():
# Get the name of the Python script
    result={}
    quadrants = [[0,0],[0,0]]
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    fig, ax = plt.subplots()
    for maximum in tqdm.trange(10000):
        data = [[0 for _ in range(MAX_X)] for _ in range(MAX_Y)]
        with open(input_file) as f:
            for line in f.readlines():
                line = line.strip()
                if line == '#':
                    break
                m = line.split()
                point = [int(x) for x in m[0].split('=')[1].split(',')]
                vector = [int(x) for x in m[1].split('=')[1].split(',')]
                #robot = get_destination(point,vector,(101,103))
                robot = get_destination(point,vector,(MAX_X,MAX_Y),maximum)
                if robot[0] != (MAX_X-1)/2:
                    if robot[1] != (MAX_Y-1)/2:
                        if robot[0] < MAX_X/2:
                            if robot[1] < MAX_Y/2:
                                quadrants[0][0]+=1
                            else:
                                quadrants[1][0]+=1
                        else:
                            if robot[1] < MAX_Y/2:
                                quadrants[0][1]+=1
                            else:
                                quadrants[1][1]+=1
                    ""
                data[robot[1]][robot[0]]=1 if data[robot[1]][robot[0]]=='.' else data[robot[1]][robot[0]]+1
        
        array = np.array(data)
        entropy = calculate_image_entropy(array)
        result[f'{entropy:.4f}'] = (maximum,array)
        #print(entropy)
        # plt.imshow(array, cmap="binary", interpolation="nearest")
        # plt.axis("off")  # Hide axis labels
        # plt.title(f"Raster Image {maximum} s")
        # plt.pause(0.5)
        # plt.clf()
        # plt.ioff()
    #time.sleep(5)
    print(sorted(result.keys())[:6])
    for d in sorted(result.keys())[:6]:
        plt.imshow(result[d][1], cmap="binary", interpolation="nearest")
        plt.axis("off")  # Hide axis labels
        plt.title(f"Raster Image {d} ({result[d][0]} seconds)")
        plt.show()
        # plt.clf()
        # plt.ioff()
    
    print('Endo',quadrants[0][0]*quadrants[0][1]*quadrants[1][0]*quadrants[1][1])
if __name__ == '__main__':
    main()
# 4664 .. too low
# 9449 .. too high
# 9714