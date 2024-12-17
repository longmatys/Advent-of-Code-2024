""" Advent of code day 17 """
import os
import logging
import re
import math


class Computer:
    """ Computer representing whole program logic """
    instructions = ['adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv']

    def __init__(self, a=0, b=0, c=0, program=None):
        self.a = a
        self.b = b
        self.c = c
        if program is None:
            self.program = []
        else:
            self.program = program
        self.program = program
        self.pc = 0
        self.output = []

    def adv(self):
        """ 0 """
        self.a = math.floor(self.a/(2**self.get_combo_operand()))
        self.pc += 2

    def bxl(self):
        """ 1 """
        self.b = self.b ^ self.program[self.pc+1]
        self.pc += 2

    def bst(self):
        """ 2 """
        self.b = self.get_combo_operand() % 8
        self.pc += 2

    def jnz(self):
        """ 3 """
        if self.a == 0:
            self.pc += 2
        else:
            self.pc = self.get_combo_operand()

    def bxc(self):
        """ 4 """
        self.b = self.b ^ self.c
        self.pc += 2

    def out(self):
        """ 5 """
        self.output.append(self.get_combo_operand() % 8)
        self.pc += 2

    def bdv(self):
        """ 6 """
        self.b = math.floor(self.a/(2**self.get_combo_operand()))
        self.pc += 2

    def cdv(self):
        """ 7 """
        self.c = math.floor(self.a/(2**self.get_combo_operand()))
        self.pc += 2

    def set_register(self, attr, value):
        """ Set registry value """
        # Check if the attribute exists before setting
        if hasattr(self, attr):
            setattr(self, attr, value)
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
a = {self.a}, b = {self.b}, c = {self.c}, pc = {self.pc}
program = {self.program}

output={','.join([str(z) for z in self.output])}
"""

    def run(self):
        """ Iterate the computer through the program """
        while 0<= self.pc < len(self.program):
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
    computer.run()
    print(computer)


if __name__ == '__main__':
    main()
