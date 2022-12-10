"""
The complete problem statement is in 9description.txt.  It is 709 lines and was
too unwieldy to include directly.
"""
import sys


class Grid(object):
    def __init__(self, size=80):
        self.size = size
        self.grid = []
        for n in range(size):
            self.grid.append(['.'] * size)

    def plot(self, x, y, name):
        self.grid[y][x] = name

    def show_grid(self):
        for n in range(self.size-1, -1, -1):
            print(''.join(self.grid[n]))


class Position(object):
    ##
    # A new aspect of the puzzle is that each motion needs to (k)not only know
    # the preceding knot's position, but also its most recent direction of
    # travel.
    # To learn that, we also need to know how to query the preceding knot.
    def __init__(self, x, y, leader, name):
        self.x = x
        self.y = y
        self.tail_positions = None
        self.leader = leader
        if name == 0:
            self.name = 'H'
        else:
            self.name = str(name)
        self.last_direction = None

    def is_tail(self):
        self.tail_positions = set()

    def up(self):
        self.y += 1

    def down(self):
        self.y -= 1

    def left(self):
        self.x -= 1

    def right(self):
        self.x += 1

    def distance(self, other):
        x_dist = other.x - self.x
        y_dist = other.y - self.y
        # Used for setting a breakpoint for debugging.
        if abs(x_dist) > 2 or abs(y_dist) > 2:
            pass
        return x_dist, y_dist

    def adjust(self):
        other = self.leader

        x_dist, y_dist = self.distance(other)
        if abs(x_dist) + abs(y_dist) == 3:
            # These all require two moves.
            if x_dist > 0:
                self.right()
            else:
                self.left()
            if y_dist > 0:
                self.up()
            else:
                self.down()
        else:
            if x_dist == 2:
                self.right()
            elif x_dist == -2:
                self.left()
            if y_dist == 2:
                self.up()
            elif y_dist == -2:
                self.down()
        if self.tail_positions is not None:
            self.tail_positions.add((self.x, self.y))

    def output_how_many_tail_positions(self):
        print(len(self.tail_positions))

    def plot_location(self, grid):
        grid.plot(self.x, self.y, self.name)


def do_adjust(positions):
    for n in range(1, 10):
        positions[n].adjust()


testing = True


def main():
    global testing
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            input_file = open('9test.txt')
        else:
            input_file = open('9btest.txt')
    else:
        input_file = open('9input.txt')
        testing = False

    # Create our 10 positions (knots)
    positions = [Position(11, 5, None, 0)]
    for n in range(1, 10):
        positions.append(Position(11, 5, positions[n-1], n))
    positions[9].is_tail()

    steps = [x.split(' ') for x in input_file.read().split('\n')]
    for step in steps:
        if step[0] == 'R':
            for n in range(int(step[1])):
                positions[0].right()
                do_adjust(positions)
        elif step[0] == 'L':
            for n in range(int(step[1])):
                positions[0].left()
                do_adjust(positions)
        elif step[0] == 'U':
            for n in range(int(step[1])):
                positions[0].up()
                do_adjust(positions)
        elif step[0] == 'D':
            for n in range(int(step[1])):
                positions[0].down()
                do_adjust(positions)
        else:
            raise Exception("Can't get here!")

        for n in range(1, 10):
            positions[n].adjust()

        if testing:
            grid = Grid(26)
            for n in range(9, -1, -1):
                positions[n].plot_location(grid)

            print('****')
            grid.show_grid()
            pass

    positions[9].output_how_many_tail_positions()


if __name__ == '__main__':
    main()
