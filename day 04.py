import os
import logging
def check_word(data,i,j,i_dir,j_dir):
    
    
    for z in 'XMAS':
        if i <0 or j <0 or i==len(data) or j==len(data[0]):
            return 0
        if data[i][j] != z:
            return 0
        i+=i_dir
        j+=j_dir
    
    return 1
def check_letter(data,i,j,letter):
    if i<0 or j<0 or i==len(data) or j==len(data[0]):
        return False
    return letter=='.' or data[i][j]==letter
        
def check_pattern(data,i,j,pattern):
    local_i = i
    
    for x,x_pattern in enumerate(pattern):
        local_j = j
        for y,letter in enumerate(x_pattern):
            if not check_letter(data,local_i,local_j,letter):
                return 0
            local_j+=1
        local_i+=1
    return 1
def part2(data):
    patterns=[
        ['M.S','.A.','M.S'],
        ['S.S','.A.','M.M'],
        ['M.M','.A.','S.S'],
        ['S.M','.A.','S.M'],
    ]
    result = 0
    for i,line in enumerate(data):
        for j,char in enumerate(line):
            for pattern in patterns:
                result +=check_pattern(data,i,j,pattern)
    print('Part 2',result)
def part1(data):
    result_1 = 0
    result_2 = 0
    for i,line in enumerate(data):
        for j,char in enumerate(line):
            for i_dir in [-1,0,1]:
                for j_dir in [-1,0,1]:
                    
                    if i_dir==0 and j_dir==0:
                        continue
                    result_1 += check_word(data,i,j,i_dir,j_dir)
                    
    print('Part 1',result_1)
                    
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    with open(input_file) as f:
        data = [ line.strip() for line in f.readlines()]
        
        part1(data)
        part2(data)
        
if __name__ == '__main__':
    main()