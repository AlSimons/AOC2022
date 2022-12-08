"""
--- Day 8: Treetop Tree House ---
The expedition comes across a peculiar patch of tall trees all planted carefully
in a grid. The Elves explain that a previous expedition planted these trees as a
reforestation effort. Now, they're curious if this would be a good location for
a tree house.

First, determine whether there is enough tree cover here to keep a tree house
hidden. To do this, you need to count the number of trees that are visible from
outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height
of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390
Each tree is represented as a single digit whose value is its height, where 0 is
the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid
are shorter than it. Only consider trees in the same row or column; that is,
only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are
already on the edge, there are no trees to block the view. In this example, that
only leaves the interior nine trees to consider:

The top-left 5 is visible from the left and top. (It isn't visible from the
right or bottom since other trees of height 5 are in the way.)
The top-middle 5 is visible from the top and right.
The top-right 1 is not visible from any direction; for it to be visible, there
would need to only be trees of height 0 between it and an edge.
The left-middle 5 is visible, but only from the right.
The center 3 is not visible from any direction; for it to be visible, there
would need to be only trees of at most height 2 between it and an edge.
The right-middle 3 is visible from the right.
In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
With 16 trees visible on the edge and another 5 visible in the interior, a total
of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?
"""

import sys
rows = 0
columns = 0
forest = None


def is_visible_north(row, column):
    my_height = forest[row][column]
    for n in range(row-1, -1, -1):
        if forest[n][column] >= my_height:
            return False
    return True


def is_visible_south(row, column):
    my_height = forest[row][column]
    for n in range(row+1, len(forest)):
        if forest[n][column] >= my_height:
            return False
    return True


def is_visible_east(row, column):
    my_height = forest[row][column]
    for n in range(column+1, len(forest[row])):
        if forest[row][n] >= my_height:
            return False
    return True


def is_visible_west(row, column):
    my_height = forest[row][column]
    for n in range(column-1, -1, -1):
        if forest[row][n] >= my_height:
            return False
    return True


def is_visible(row, column):
    return is_visible_north(row, column) or \
        is_visible_south(row, column) or \
        is_visible_east(row, column) or \
        is_visible_west(row, column)


def survey_forest():
    visible_trees = 0
    for row in range(len(forest)):
        for column in range(len(forest[0])):
            if is_visible(row, column):
                visible_trees += 1
    print(visible_trees)


def main():
    global rows, columns, forest

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        input_file = open('8test.txt')
    else:
        input_file = open('8input.txt')

    forest = input_file.read().split('\n')
    rows = len(forest)
    columns = len(forest[0])
    print(forest)
    print(rows, columns)

    survey_forest()


if __name__ == '__main__':
    main()
