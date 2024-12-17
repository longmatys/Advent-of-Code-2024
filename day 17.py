""" Advent of code day 17 """
import os
import logging
import re
import math
import tqdm
from concurrent.futures import ProcessPoolExecutor
import copy


class Computer:
    """ Computer representing whole program logic """
    instructions = ['adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv']

    def __init__(self, a=0, b=0, c=0, program=None):
        self.a = a
        self.b = b
        self.c = c
        self.orig_a = self.a
        self.orig_b = self.b
        self.orig_c = self.c
        self.clock = 0
        if program is None:
            self.program = []
        else:
            self.program = program
        self.program = program
        self.pc = 0
        self.output = []

    def reset(self):
        """ Reset to the original state"""
        self.a = self.orig_a
        self.b = self.orig_b
        self.c = self.orig_c
        self.pc = 0
        self.output = []
        self.clock = 0

    def adv(self):
        """ 0 """
        self.a = math.floor(self.a/(2**self.get_combo_operand()))
        self.pc += 2
        self.clock += 1

    def bxl(self):
        """ 1 """
        self.b = self.b ^ self.program[self.pc+1]
        self.pc += 2
        self.clock += 1

    def bst(self):
        """ 2 """
        self.b = self.get_combo_operand() % 8
        self.pc += 2
        self.clock += 1

    def jnz(self):
        """ 3 """
        if self.a == 0:
            self.pc += 2
        else:
            self.pc = self.get_combo_operand()
        self.clock += 1

    def bxc(self):
        """ 4 """
        self.b = self.b ^ self.c
        self.pc += 2
        self.clock += 1

    def out(self):
        """ 5 """
        self.output.append(self.get_combo_operand() % 8)
        self.pc += 2
        self.clock += 1

    def bdv(self):
        """ 6 """
        self.b = math.floor(self.a/(2**self.get_combo_operand()))
        self.pc += 2
        self.clock += 1

    def cdv(self):
        """ 7 """
        self.c = math.floor(self.a/(2**self.get_combo_operand()))
        self.pc += 2
        self.clock += 1

    def set_register(self, attr, value):
        """ Set registry value """
        # Check if the attribute exists before setting
        if hasattr(self, attr):
            setattr(self, attr, value)
            setattr(self, f'orig_{attr}', value)
        else:
            raise AttributeError(
                f"'{attr}' is not a valid attribute of Computer"
                )

    def set_program(self, program):
        """ Set the computer program """
        self.program = program

    def __repr__(self):
        """ Just to print current state"""
        return f"""
Computer:
a = {self.a}
b = {self.b}
c = {self.c}
clock = {self.clock}

pc = {self.pc}

program = {self.program}

output={','.join([str(z) for z in self.output])}
"""

    def run(self):
        """ Iterate the computer through the program """
        while 0 <= self.pc < len(self.program) and \
                len(self.program) >= len(self.output):
            getattr(self, self.instructions[self.program[self.pc]])()

    def get_combo_operand(self):
        """ Returns operand based on combo operand value """
        combo = self.program[self.pc+1]
        if 0 <= combo < 4:
            return combo
        if combo == 4:
            return self.a
        if combo == 5:
            return self.b
        if combo == 6:
            return self.c
        assert False, f"Invalid combo operand {combo}"


# Worker function to process part of the range
def worker(start, end, computer, thread_id):
    for a in tqdm.tqdm(range(start, end), 
                       desc=f"Process-{thread_id}", position=thread_id):
        computer.reset()  # Reset the computer to its default state
        computer.set_register("a", a)
        
        computer.run()
        if computer.program == computer.output:
            print(f"Solution found by Process-{thread_id}: {a}")
            return a  # Return the solution


# Split the range into chunks and run processes
def split_and_run(total, computer_instance, num_processes=8):
    part_size = total // num_processes  # Calculate size of each chunk
    ranges = [(i * part_size, (i + 1) * part_size) 
              for i in range(num_processes)]
    # Ensure last range covers any remainder
    ranges[-1] = (ranges[-1][0], total)  

    # Create independent copies of the computer instance for each process
    computer_copies = [copy.deepcopy(computer_instance) for _ in range(num_processes)]

    # Launch processes with their assigned range and independent computer instance
    
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [
            executor.submit(worker, start, end, computer_copies[thread_id], thread_id)
            for thread_id, (start, end) in enumerate(ranges)
        ]

        # Check for results
        for future1 in futures:
            result = future1.result()
            if result is not None:
                print(f"Solution found: {result}")
                executor.shutdown(wait=False)
                break
#@cache
def find_solution(output=2,final_a=0,limit=100):
    
    res = []
    for A in  range(final_a*8,final_a*8+8):
        # Step 1: Calculate (A % 8)
        result,result_a = test_it(A)
        
        # Check if result equals 2
        if result == output and result_a == final_a:
            res.append(A)
            print(f"Solution found: A = {A} ({output}, {final_a})")
            #return res
    return res
#@cache
def test_it(a, debug=False):
    if debug:
        print(f'For input a={a}: ',end='')
    b = a % 8
    b = b ^ 1
    c = math.floor(a / (2**b))
    b = b ^ 5
    b = b ^ c
    out = b % 8
    a = math.floor(a/2**3)
    if debug:
        print(out,a)
    return out,a

def main():
    """ Main program """
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG,
                        format='%(funcName)s (%(lineno)d): %(message)s'
                        )
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    computer = Computer()
    with open(input_file, 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == '#':
                continue
            m = re.search(r'Register (.): (\d+)', line)
            if m:
                computer.set_register(m[1].lower(), int(m[2]))
            m = re.search(r'Program: (.*)', line)
            if m:
                computer.set_program([int(z) for z in m[1].split(',')])
    TOTAL = 1200000000  # Total range
    # Brute force split_and_run
    #split_and_run(TOTAL, computer)
    # for a in tqdm.trange(1200000000):
    #     computer.set_register("a", a)
    #     computer.reset()

    #     computer.run()
    #     if computer.program == computer.output:
    #         print(f'Solution found: {a}')
    candidates_new = [0]
    for i,res_out in enumerate(reversed(computer.program)):
        print(f'Trying to find {res_out}')
        candidates = candidates_new
        candidates_new = []
        for candidate in candidates:
            for sol in find_solution(res_out,candidate,10**8):
            
                computer.set_register("a", sol)
                computer.reset()

                computer.run()
                candidates_new.append(sol)
                print(f'Result for A={sol}, desired result {computer.program[-(i+1):]} : {computer.output}')
    print(candidates_new)
if __name__ == '__main__':
    main()
