import os
import logging
import re
import math
import tqdm

from sympy import symbols, Eq, solve


BUTTON_A_COST = 3
BUTTON_B_COST = 1
PART2 = 10000000000000
def work2(button_a,button_b,prize):
    a, b = symbols('a b', integer=True)
    # Equations for X and Y
    eq1 = Eq(button_a[0] * a + button_b[0] * b, prize[0])  # X
    eq2 = Eq(button_a[1] * a + button_b[1] * b, prize[1])  # Y
    # Solve equations with general solution
    solutions = solve((eq1, eq2), (a, b), dict=True)
    assert len(solutions)<=1, "I expect 1 solution at most"
    if len(solutions):
        result = solutions[0][a]*BUTTON_A_COST+solutions[0][b]*BUTTON_B_COST
        return result
    return None
    
def work(button_a,button_b,prize):
    
    result = set()
    for x in range(100):
        result.update( [(x*BUTTON_A_COST+y*BUTTON_B_COST,x,y)  for y in range(100) if (button_a[0]*x+button_b[0]*y==prize[0]) and (button_a[1]*x+button_b[1]*y==prize[1])])
        
    if len(result):
        return list(result)[0][0]
    return None
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    data = []
    with open(input_file) as f:
        while(True):
            a = f.readline()
            if a=='':
                break
            if a.strip()=='':
                continue
            b = f.readline()
            p = f.readline()
            button_a = [int(x) for x in re.findall(r'(\d+).*\+(\d+)',a)[0]]
            button_b = [int(x) for x in re.findall(r'(\d+).*\+(\d+)',b)[0]]
            prize = [int(x) for x in re.findall(r'(\d+).*=(\d+)',p)[0]]
            data.append((button_a,button_b,prize))
    counter1 = 0
    counter2 = 0
    for (button_a,button_b,prize) in tqdm.tqdm(data,desc='Part 1'):
        if res := work2(button_a,button_b,prize):
            counter1+=res
        if res := work2(button_a,button_b,(prize[0]+PART2,prize[1]+PART2)):
            counter2+=res

    print(f'Min tokens Part 1: {counter1}')
    print(f'Min tokens Part 2: {counter2}')
    
if __name__ == '__main__':
    main()