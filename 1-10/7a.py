"""
--- Day 7: No Space Left On Device ---
You can hear birds chirping and raindrops hitting leaves as the expedition
proceeds. Occasionally, you can even hear much louder sounds in the distance;
how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication
system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device
Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting
terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
The filesystem consists of a tree of files (plain data) and directories (which
can contain other directories or files). The outermost directory is called /.
You can navigate around the filesystem, moving into or out of directories and
listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed,
very much like some modern computers:

cd means change directory. This changes which directory is the current
directory, but the specific result depends on the argument:
cd x moves in one level: it looks in the current directory for the directory
named x and makes it the current directory.
cd .. moves out one level: it finds the directory that contains the current
directory, then makes that directory the current directory.
cd / switches the current directory to the outermost directory, /.
ls means list. It prints out all of the files and directories immediately
contained by the current directory:
123 abc means that the current directory contains a file named abc with size
123.
dir xyz means that the current directory contains a directory named xyz.
Given the commands and output in the example above, you can determine that the
filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
Here, there are four directories: / (the outermost directory), a and d (which
are in /), and e (which is in a). These directories also contain files of
various sizes.

Since the disk is full, your first step should probably be to find directories
that are good candidates for deletion. To do this, you need to determine the
total size of each directory. The total size of a directory is the sum of the
sizes of the files it contains, directly or indirectly. (Directories themselves
do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

The total size of directory e is 584 because it contains a single file i of size
584 and no other directories.
The directory a has total size 94853 because it contains files f (size 29116), g
(size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which
contains i).
Directory d has total size 24933642.
As the outermost directory, / contains every file. Its total size is 48381165,
the sum of the size of every file.
To begin, find all of the directories with a total size of at most 100000, then
calculate the sum of their total sizes. In the example above, these directories
are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this
example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum
of the total sizes of those directories?
"""

###
# A recursive descent parser.  Sometimes this is the basis of a compiler
# front end.
#

import sys


class Directory(object):
    def __init__(self, name, parent=None):
        # Turns out we're never asked for the name, but what the heck.
        self.name = name
        self.parent = parent
        self.child_dirs = []
        self.files = set()
        self.total_size = 0
        if parent is not None:
            parent.child_dirs.append(self)

    def add_file(self, name, size):
        self.files.add(name)
        self.add_file_size(size)

    def add_file_size(self, size):
        self.total_size += size
        if self.parent is not None:
            self.parent.add_file_size(size)

    def get_child_dir_by_name(self, child_dir_name):
        for child_dir in self.child_dirs:
            if child_dir.name == child_dir_name:
                return child_dir

    def total_qualified_size(self):
        total_qual_size = 0
        # Get the sum of all the qualified child directories' sizes.
        for child_dir in self.child_dirs:
            total_qual_size += child_dir.total_qualified_size()
        if self.total_size <= 100000:
            total_qual_size += self.total_size
        return total_qual_size

    def get_root_dir(self):
        me = self
        while me.parent is not None:
            me = parent
        return me


def cd(directory, line):
    """
    Traverse the directory tree.  Note that in the input there is no
    cd command with two levels, e.g., cd foo/bar.  This routine handles
    the case where the desired command already exists in the tree.
    :param directory: The current directory from which we are cd-ing.
    :param line: The file line containing the cd command.
    :return: The resultant directory.
    """
    next_directory_name = line.strip().split(' ')[2]
    if next_directory_name == '..':
        # Going up a level
        if directory.parent is None:
            # The parent of / is /
            return directory
        return directory.parent

    if next_directory_name == '/':
        return directory.get_root_dir()

    # Descending a level
    return directory.get_child_dir_by_name(next_directory_name)


def record_ls_data(directory, line):
    """
    Record the contents of a directory.
    :param directory: The current directory
    :param line: The ls output line
    :return: Nothing, the directory is updated.
    """
    if line.startswith('dir'):
        # Create a directory entry that we can traverse into.
        Directory(line.strip().split()[1], directory)
    else:
        if not line.strip():
            pass
        size, name = line.strip().split()
        directory.add_file(name, int(size))


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        input_file = open('7test.txt')
    else:
        input_file = open('7input.txt')

    # Initialize our directory tree with the root directory, which always
    # exists.
    root_directory = Directory('/')
    directory = root_directory

    in_ls_output = False
    while True:
        line = input_file.readline()
        if not line.strip():
            break
        if line.startswith('$'):
            in_ls_output = False
        if line.startswith('$ cd'):
            directory = cd(directory, line)
        elif line.startswith('$ ls'):
            in_ls_output = True
        elif in_ls_output:
            record_ls_data(directory, line)

    # Done processing the input. Report the dirs as requested.
    print(root_directory.total_qualified_size())


if __name__ == '__main__':
    main()
