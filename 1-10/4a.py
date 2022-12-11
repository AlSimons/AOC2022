"""
--- Day 4: Camp Cleanup ---
Space needs to be cleared before the last supplies can be unloaded from the ships, and so several Elves have been assigned the job of cleaning up sections of the camp. Every section has a unique ID number, and each Elf is assigned a range of section IDs.

However, as some of the Elves compare their section assignments with each other, they've noticed that many of the assignments overlap. To try to quickly find overlaps and reduce duplicated effort, the Elves pair up and make a big list of the section assignments for each pair (your puzzle input).

For example, consider the following list of section assignment pairs:

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
For the first few pairs, this list means:

Within the first pair of Elves, the first Elf was assigned sections 2-4 (sections 2, 3, and 4), while the second Elf was assigned sections 6-8 (sections 6, 7, 8).
The Elves in the second pair were each assigned two sections.
The Elves in the third pair were each assigned three sections: one got sections 5, 6, and 7, while the other also got 7, plus 8 and 9.
This example list uses single-digit section IDs to make it easier to draw; your actual list might contain larger numbers. Visually, these pairs of section assignments look like this:

.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8
Some of the pairs have noticed that one of their assignments fully contains the other. For example, 2-8 fully contains 3-7, and 6-6 is fully contained by 4-6. In pairs where one assignment fully contains the other, one Elf in the pair would be exclusively cleaning sections their partner will already be cleaning, so these seem like the most in need of reconsideration. In this example, there are 2 such pairs.

In how many assignment pairs does one range fully contain the other?
"""


import sys


def get_range(assignment):
    low, high = assignment.split('-')
    return range(int(low), int(high) + 1)


def parse_line(line):
    # Returns two sets of locations indicating the two cleanup assignments
    line = line.strip()
    assignments = line.split(',')
    first_assignment_set = set(get_range(assignments[0]))
    second_assignment_set = set(get_range(assignments[1]))
    return first_assignment_set, second_assignment_set


def completely_contained(first_assignment_set, second_assignment_set):
    return len(first_assignment_set - second_assignment_set) == 0 or \
           len(second_assignment_set - first_assignment_set) == 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        input_file = open('4test.txt')
    else:
        input_file = open('4input.txt')
    num_completely_contained = 0
    for line in input_file:
        first_assignment_set, second_assignment_set = \
            parse_line(line)
        if completely_contained(first_assignment_set, second_assignment_set):
            num_completely_contained += 1
    print(num_completely_contained)


if __name__ == '__main__':
    main()
