"""
Description in 13description.txt; too long to include here.
"""


import sys

INORDER = 0
SAME = 1
OUTOFORDER = 2


def compare_ints(left, right):
    if left < right:
        return INORDER
    if left == right:
        return SAME
    # Only thing left is left > right, don't need to test.
    return OUTOFORDER


def compare_lists(left, right):
    lr_types = (type(left), type(right))
    if lr_types == (int, int):
        return compare_ints(left, right)
    elif lr_types == (int, list):
        return compare_lists([left], right)
    elif lr_types == (list, int):
        return compare_lists(left, [right])

    # Now we have to process the complicated case: two lists.
    # Compare the first items:
    left_empty = False
    right_empty = False
    try:
        l_pop = left.pop(0)
    except IndexError:
        left_empty = True
    try:
        r_pop = right.pop(0)
    except IndexError:
        right_empty = True
    if left_empty and not right_empty:
        return INORDER
    if not left_empty and right_empty:
        return OUTOFORDER
    if left_empty and right_empty:
        # We exhausted both lists at the same time.
        return SAME

    # OK, we've successfully gotten items to compare.
    compare_value = compare_lists(l_pop, r_pop)
    if compare_value != SAME:
        return compare_value

    # The lists are now stripped of their first elements, compare the remainder.
    return compare_lists(left, right)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        input_file = open('13test.txt')
    else:
        input_file = open('13input.txt')

    pair_index = 0
    in_order_indices = []
    while True:
        pair_index += 1
        left_line = input_file.readline().strip()
        if not left_line:
            break
        right_line = input_file.readline().strip()
        # Get rid of the blank line.
        input_file.readline()
        print("LL:", left_line, file=sys.stderr)
        print("RL:", right_line, file=sys.stderr)
        left = eval(left_line)
        right = eval(right_line)
        print(left)
        print(right)
        compare_value = compare_lists(left, right)
        print(compare_value)
        if compare_value == INORDER:
            in_order_indices.append(pair_index)

    print(sum(in_order_indices))


if __name__ == '__main__':
    main()
