import os
import logging
import tqdm
import itertools
# 90542694500 .. too low
# 6367087064415
# 6390781891880
# 9139537948329 .. too high
def populate_disk(line):
    data=True
    data_i=0
    for char in line:
        if data:
            disk_sector = str(data_i)
            
            data_i+=1
        else:
            disk_sector = '.'
        yield [ disk_sector for _ in range(int(char))]
        data = not data
def populate_disk2(line):
    data=True
    data_i=0
    disk_position = 0
    for char in line:
        if data:
            data_value = data_i            
            data_i+=1
        else:
            data_value = -1
        yield  [disk_position,int(char),data_value]
        data = not data
        disk_position += int(char)
def get_char_backwards(disk,char,start):
    for i in range(start,len(disk)+1):
        if char != disk[-i]:
            return i
    return None
def move_data(free_space,data):
    for i,v in enumerate(free_space):
        if v[0]>=data[0]:
            #free space is behind actual data
            return
        if v[1]>=data[1]:
            #great it fits            
            data[0]=v[0]
            v[1] -= data[1]
            v[0] += data[1]
            return 
    
def part2(line):
    
    disk = list(populate_disk2(line))
    
    free_space = [item for item in disk if item[2]==-1]
    occupied_space = [item for item in disk if item[2]!=-1]
    for os_i in tqdm.trange(len(occupied_space)):
        move_data(free_space,occupied_space[-(os_i+1)])
    result = 0
    for data in occupied_space:
        for sector_i in range(data[0],data[0]+data[1]):
            result += sector_i * data[2]
    print("Part 2:",result)
   
    ""
    
    
def part1(line):
    disk = [item for sublist in populate_disk(line) for item in sublist]
    disk_ids = sorted([int(item) for item in disk if item!='.'])
    #print(''.join(disk),len(disk))
    
    data_i = 0
    #while free_i := disk.index('.'):
    for free_i in tqdm.trange(len(disk)):
        if disk[free_i] == '.':
            data_i = get_char_backwards(disk,'.',data_i+1)
            if data_i>=len(disk) - free_i-1 :
                break
            disk[free_i] = disk[-data_i]
            disk[-data_i] = '.'
            #print(''.join(disk),len(disk))
    #print(disk)
    print('Part 1:',sum([i*int(v) for i,v in enumerate(disk) if v!='.'] ))
    #print(''.join(disk),len(disk))
    
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '#':
                break
            
            res = part1(line)
            res = part2(line)
if __name__ == '__main__':
    main()