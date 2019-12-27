from intcode import Computer
from collections import defaultdict
from day11 import run_intcode

import sys


class AComputer(Computer):
    def __init__(self, program, other_computers, address):
        self.other_computers = other_computers
        self.i = 0
        self.input_queue = [address]
        self.out_memory = []
        super().__init__(program)

    def get_input(self):
        if self.i >= len(self.input_queue):
            return -1
        x = self.input_queue[self.i]
        self.i += 1
        return x

    def process_output(self, o):
        self.out_memory.append(o)
        if len(self.out_memory) % 3 == 0:
            address, x, y = self.out_memory
            if address == 255:
                print(y)
                sys.exit()
            self.out_memory = []
            self.other_computers[address].input_queue.append(x)
            self.other_computers[address].input_queue.append(y)


def a(program):
    computers = []
    computers.extend([AComputer(program, computers, i) for i in range(50)])
    while True:
        for computer in computers:
            computer.run(1)


class BComputer(Computer):
    def __init__(self, program, other_computers, address, NAT):
        self.other_computers = other_computers
        self.i = 0
        self.input_queue = [address]
        self.out_memory = []
        self.NAT = NAT
        self.idle = False
        super().__init__(program)

    def get_input(self):
        if self.i >= len(self.input_queue):
            self.idle = True
            return -1
        self.idle = False
        x = self.input_queue[self.i]
        self.i += 1
        return x

    def process_output(self, o):
        self.out_memory.append(o)
        if len(self.out_memory) % 3 == 0:
            address, x, y = self.out_memory
            if address == 255:
                self.NAT[0] = x
                self.NAT[1] = y
            else:
                self.other_computers[address].input_queue.append(x)
                self.other_computers[address].input_queue.append(y)
            self.out_memory = []


def b(program):
    nat_packet = [None, None]
    computers = []
    computers.extend([BComputer(program, computers, i, nat_packet) for i in range(50)])
    prev_y = None
    while True:
        for computer in computers:
            computer.run(1)
        if all(computer.idle for computer in computers) and None not in nat_packet:
            if nat_packet[1] == prev_y:
                return prev_y
            prev_y = nat_packet[1]
            computers[0].input_queue.append(nat_packet[0])
            computers[0].input_queue.append(nat_packet[1])
            nat_packet[0] = None


def main():
    program = list(map(int, open("input23.txt").read().split(",")))
    print(b(program))


if __name__ == "__main__":
    main()
