import os
import logging
import tqdm
from llist import dllist
import time
from functools import cache
from line_profiler import LineProfiler
from math import floor, log10




class MyCache:
    data={}
    @cache
    @staticmethod
    #@profile
    def get_next(number):
        if number == 0:
            return [1]
        elif len(str(number))%2 == 1:
            return [number * 2024]
        else:
            str_v = str(number)
            second = int(str_v[int(len(str_v)/2):])
            first = int(str_v[:int(len(str_v)/2)])
            return [first,second]            
    #@profile        
    def update(self,number,depth):
        try:
            dat = self.data.get(number,{"childs":[],"depths":[0]*depth})
            #if len(dat["depths"])<depth:
            dat["depths"]+= [0]*(depth-len(dat["depths"]))
            if depth > 0 and dat["depths"][depth-1]==0 :
                res = MyCache.get_next(number)
                dat["childs"]=res
                childs_len = 0
                for child in res:
                    childs_len += self.update(child,depth-1)
                dat["depths"][-1] = childs_len
                
                self.data[number] = dat
                return childs_len
            else:
                if depth == 0:
                    return 1
                return dat["depths"][depth-1]
        except:
            print()
           
    def __init__(self,parents,depth):
        self.cache_len = 0
        self.start = parents
        for parent in parents:
            self.cache_len += self.update(parent,depth)
    def unfold(self,parents,clicks):
        ret = []
        if clicks==0:
            return parents
        for parent in parents:
            ret += self.unfold(self.data[parent]["childs"],clicks-1)
        return ret
            
                
            
        
        
def blick(line):
    i=0
    while i<len(line):
        if line[i] == 0:
            line[i] = 1
        elif len(str(line[i]))%2 == 1:
            line[i] = line[i]*2024
        else:
            str_v = str(line[i])
            line[i] = int(str_v[:int(len(str_v)/2)])
            if i+1 == len(line):
                line.append(int(str_v[int(len(str_v)/2):]))
            else:
                a = line.nodeat(i+1)
                line.insert(int(str_v[int(len(str_v)/2):]),line.nodeat(i+1))
            i+=1
        #if len(line)%10000 == 0:
        #    print(len(line))
        i+=1
#@profile
def part1(data,blicks):
    line = [int(el) for el in data.split()]
    
    cache = MyCache(line,blicks)
    
    #print("Unfolded",len(cache.unfold(line,blicks)),cache.unfold(line,blicks))
    #print(f"Debug: {cache.cache_len}",cache.unfold(line,blicks))
    return len(cache.unfold(line,blicks))
def part1_simple(data,blicks):
    line = dllist([int(el) for el in data.split()])
    #print(line)
    pbar = tqdm.trange(blicks,mininterval=0.1,maxinterval=0.5,miniters=1)
    for _ in pbar:
        #print(len(line))
        blick(line)
    #print(line)
    return len(line)
@cache
def compute(number,clicks):
    if clicks==0:
        return 1
    res = MyCache.get_next(number)
    childs_len = 0
    for child in res:
        childs_len += compute(child,clicks-1)
    return childs_len
@cache
def part1_cache(data,blicks):
    #My solution, pretty fast
    line = [int(el) for el in data.split()]
    ret = 0
    for i in line:
        ret+=compute(i,blicks)
    return ret
@cache
def count(x, d=75):
    if d == 0: return 1
    if x == 0: return count(1, d-1)

    l = floor(log10(x))+1
    if l % 2: return count(x*2024, d-1)

    return (count(x // 10**(l//2), d-1)+
            count(x %  10**(l//2), d-1))
def part2_external(data,blicks):
    #Internet solution, slower
    line = map(int, data.split())
    return sum(map(count, line))
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
            #print(line)
            clicks=75
            print(f'Starting with {clicks} clicks')
            start_time = time.time()
            res = part2_external(line,clicks)
            end_time = time.time()
            print(f'Part 2 External: {res} stones ({end_time - start_time:.4f} seconds)')
            start_time = time.time()
            res = part1_cache(line,clicks)
            end_time = time.time()
            print(f'Part 1 Cache: {res} stones ({end_time - start_time:.4f} seconds)')
            #start_time = time.time()
            #res = part1(line,clicks)
            #end_time = time.time()
            #print(f'Part 1 Complex: {res} stones ({end_time - start_time:.4f} seconds)')
            #start_time = time.time()
            #res = part1_simple(line,clicks)
            #end_time = time.time()
            #print(f'Part 1 Simple: {res} stones ({end_time - start_time:.4f} seconds)')
            
if __name__ == '__main__':
    main()