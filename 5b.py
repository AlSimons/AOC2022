"""
--- Day 5: Supply Stacks ---
The expedition can depart as soon as the final supplies have been unloaded from
the ships. Supplies are stored in stacks of marked crates, but because the
needed supplies are buried under many other crates, the crates need to be
rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To
ensure none of the crates get crushed or fall over, the crane operator will
rearrange them in a series of carefully-planned steps. After the crates are
rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate
procedure, but they forgot to ask her which crate will end up where, and they
want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the
rearrangement procedure (your puzzle input). For example:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
In this example, there are three stacks of crates. Stack 1 contains two crates:
crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates;
from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a
single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a
quantity of crates is moved from one stack to a different stack. In the first
step of the above rearrangement procedure, one crate is moved from stack 2 to
stack 1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3
In the second step, three crates are moved from stack 1 to stack 3. Crates are
moved one at a time, so the first crate to be moved (D) ends up below the
second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3
Then, both crates are moved from stack 2 to stack 1. Again, because crates are
moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3
Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3
The Elves just need to know which crate will end up on top of each stack; in
this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3,
so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each
stack?
"""

import sys
from collections import deque
import re


class StackWithGrouping(deque):
    def push(self, item):
        self.append(item)

    def push_in_order(self, item_list):
        for n in range(len(item_list)-1, -1, -1):
            self.push(item_list[n])

    def pop_in_order(self, n):
        popped = []
        for i in range(n):
            popped.append(self.pop())
        return popped

    def get_top(self):
        return self[-1]


def make_stacks(n):
    stacks = []
    for n in range(n):
        stacks.append(StackWithGrouping())
    return stacks


def process_initial_layout(stacks, input_file):
    while True:
        line = input_file.readline()
        if '[' not in line:
            # We're done processing the initial layout
            break
        for n in range(len(stacks)):
            try:
                crate = line[n * 4 + 1]
            except IndexError:
                break  # The line didn't have all the stacks represented.
                       # Break the for loop, not the while
            if crate != ' ':
                stacks[n].push(crate)
    # Done with the initial crate/stacks setup. Consume one empty line
    # to get ready for processing the restacking instructions.
    input_file.readline()

    # Note that the input file was organized in a way that the stacks are
    # backwards; the most recently read / pushed should be at the bottom of
    # the stack.
    for stack in stacks:
        stack.reverse()


re_pattern = r'move (\d+) from (\d) to (\d)'


def process_move_instructions(stacks, input_file):
    while True:
        line = input_file.readline().strip()
        if not line:
            break
        match = re.match(re_pattern, line)
        num_to_move = int(match.group(1))
        source_stack = int(match.group(2)) - 1
        dest_stack = int(match.group(3)) - 1
        crates = stacks[source_stack].pop_in_order(num_to_move)
        stacks[dest_stack].push_in_order(crates)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        input_file = open('5test.txt')
        num_stacks = 3
    else:
        input_file = open('5input.txt')
        num_stacks = 9

    stacks = make_stacks(num_stacks)

    process_initial_layout(stacks, input_file)

    process_move_instructions(stacks, input_file)

    # Build a string from the top crate of each stack.
    result = ''
    for stack in stacks:
        result += stack.get_top()
    print(result)
    # That's all she wrote


if __name__ == '__main__':
    main()
