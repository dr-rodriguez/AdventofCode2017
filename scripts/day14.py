"""
--- Day 14: Disk Defragmentation ---
Suddenly, a scheduled job activates the system's disk defragmenter.
Were the situation different, you might sit and watch it for a while,
but today, you just don't have that kind of time.
It's soaking up valuable system resources that are needed elsewhere,
and so the only option is to help it finish its task as soon as possible.

The disk in question consists of a 128x128 grid; each square of the grid is either free or used.
On this disk, the state of the grid is tracked by the bits in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a single row in the grid;
each hash contains 128 bits which correspond to individual grid squares.
Each bit of a hash indicates whether that square is free (0) or used (1).

The hash inputs are a key string (your puzzle input), a dash, and a number from 0 to 127 corresponding to the row.
For example, if your key string were flqrgnkx,
then the first row would be given by the bits of the knot hash of flqrgnkx-0,
the second row from the bits of the knot hash of flqrgnkx-1, and so on until the last row, flqrgnkx-127.

The output of a knot hash is traditionally represented by 32 hexadecimal digits;
each of these digits correspond to 4 bits, for a total of 4 * 32 = 128 bits.
To convert to bits, turn each hexadecimal digit to its equivalent binary value, high-bit first:
0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111, and so on;
a hash that begins with a0c2017... in hexadecimal would begin with 10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx appear as follows,
 using # to denote used squares, and . to denote free ones:

##.#.#..-->
.#.#.#.#
....#.#.
#.#.##.#
.##.#...
##..#..#
.#...#..
##.#.##.-->
|      |
V      V
In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?

Your puzzle input is ugkiagan.
"""

import numpy as np


def knot_hash(my_input):

    def get_xor(x):
        a = 0
        for i in range(len(x)):
            a ^= x[i]
        return a

    def reverse_arr(l, ind, length):
        if length > len(l):
            return l

        temp = l.copy()
        if ind + length > len(l):
            find = len(l)
            diff = (ind + length) - len(l)
            t2 = temp[0:diff]
        else:
            diff = 0
            find = ind + length
            t2 = []

        t1 = temp[ind:find]
        t = np.append(t1, t2)[::-1]
        temp[ind:find] = t[0:find - ind]
        temp[0:diff] = t[find - ind:]

        return temp

    # constructing ascii set of lengths
    lengths = [ord(s) for s in my_input] + [17, 31, 73, 47, 23]
    ind = 0
    skip = 0
    arr = np.arange(256)

    # 64 rounds of basic reversing
    for i in range(64):
        for v in lengths:
            # print(arr, ind, arr[ind], skip, v)
            arr = reverse_arr(arr, ind, v)
            ind = (ind + skip + v) % len(arr)
            skip += 1

    # xor of 16 blocks
    temp = []
    for i in range(16):
        t = get_xor(arr[i * 16:(i + 1) * 16])
        temp.append(t)

    # convert to hexadecimal
    # ans = ''.join([hex(s) for s in temp])  # fails, use string format instead
    ans = ''.join(['{:02x}'.format(s) for s in temp])

    return ans

test_input = 'flqrgnkx'
my_input = test_input
my_input = 'ugkiagan'
count = 0
grid = []
for i in range(128):
    kh = knot_hash('{}-{}'.format(my_input, i))
    line = ''.join(['{:04b}'.format(int(s,16)) for s in kh])
    count += line.count('1')
    grid.append([int(s) for s in line])
print(count)

"""
--- Part Two ---
Now, all the defragmenter needs to know is the number of regions.
A region is a group of used squares that are all adjacent, not including diagonals.
Every used square is in exactly one region: lone used squares form their own isolated regions,
while several adjacent squares all count as a single region.

In the example above, the following nine regions are visible, each marked with a distinct digit:

11.2.3..-->
.1.2.3.4
....5.6.
7.8.55.9
.88.5...
88..5..8
.8...8..
88.8.88.-->
|      |
V      V
Of particular interest is the region marked 8; while it does not appear contiguous in this small view,
all of the squares marked 8 are connected when considering the whole 128x128 grid.
In total, in this example, 1242 regions are present.

How many regions are present given your key string?
"""

# My code did not work, probably since I needed to recursively iterate and set adjacent-to-adjacent in region_dict
# region BAD
def check_adjacent(i, j):
    global grid
    global region_dict

    if i-1 >= 0:
        v1 = grid[i - 1][j]
    else:
        v1 = 0

    try:
        v2 = grid[i+1][j]
    except IndexError:
        v2 = 0

    if j-1 >= 0:
        v3 = grid[i][j - 1]
    else:
        v3 = 0

    try:
        v4 = grid[i][j+1]
    except IndexError:
        v4 = 0

    x1 = region_dict.get((i - 1, j), 0)
    x2 = region_dict.get((i + 1, j), 0)
    x3 = region_dict.get((i, j - 1), 0)
    x4 = region_dict.get((i, j + 1), 0)

    if x1 > 0:
        return True, i-1, j
    elif x2 > 0:
        return True, i+1, j
    elif x3 > 0:
        return True, i, j-1
    elif x4 > 0:
        return True, i, j+1
    elif v1 > 0:
        return True, i-1, j
    elif v2 > 0:
        return True, i+1, j
    elif v3 > 0:
        return True, i, j-1
    elif v4 > 0:
        return True, i, j+1
    else:
        return False, 0, 0


def set_adjacent(i, j, regnum):
    global grid
    global region_dict

    if i - 1 >= 0:
        v1 = grid[i - 1][j]
    else:
        v1 = 0

    try:
        v2 = grid[i + 1][j]
    except IndexError:
        v2 = 0

    if j - 1 >= 0:
        v3 = grid[i][j - 1]
    else:
        v3 = 0

    try:
        v4 = grid[i][j + 1]
    except IndexError:
        v4 = 0

    # Check if already set and grab lowest if present
    x1 = region_dict.get((i - 1, j), 0)
    x2 = region_dict.get((i + 1, j), 0)
    x3 = region_dict.get((i, j - 1), 0)
    x4 = region_dict.get((i, j + 1), 0)
    if x1 > 0:
        regnum = min(x1, regnum)
    if x2 > 0:
        regnum = min(x2, regnum)
    if x3 > 0:
        regnum = min(x3, regnum)
    if x4 > 0:
        regnum = min(x4, regnum)

    region_dict[(i, j)] = regnum

    if v1 > 0:
        region_dict[(i-1, j)] = regnum
    if v2 > 0:
        region_dict[(i+1, j)] = regnum
    if v3 > 0:
        region_dict[(i, j-1)] = regnum
    if v4 > 0:
        region_dict[(i, j+1)] = regnum


region_dict = {}
region_count = 1
for i in range(128):
    for j in range(128):
        val = region_dict.get((i, j), 0)

        # If already set, set adjacent ones and move on
        if val > 0:
            set_adjacent(i, j, val)
            continue

        # Check if 0 or 1
        if grid[i][j] == 0:
            continue

        # Check adjacent ones
        check, i1, j1 = check_adjacent(i, j)
        if check:
            regnum = region_dict.get((i1, j1), 0)
            if regnum == 0:
                regnum = region_count
                region_count += 1
                region_dict[(i1, j1)] = regnum
            region_dict[(i, j)] = regnum
            set_adjacent(i, j, regnum)
        else:
            region_count += 1
            region_dict[(i, j)] = region_count
            set_adjacent(i, j, region_count)
print(region_count)
# 1529 is too high
# endregion

# Using some reddit help for a Deep First Search across the grid
# Should have realized I could do something like this given last year's puzzles
seen = set()
def dfs(i, j):
    global seen
    global grid
    if (i, j) in seen:
        return
    if not grid[i][j]:
        return
    seen.add((i, j))
    if i > 0:
        dfs(i-1, j)
    if j > 0:
        dfs(i, j-1)
    if i < 127:
        dfs(i+1, j)
    if j < 127:
        dfs(i, j+1)

region_count = 0
for i in range(128):
    for j in range(128):
        if (i,j) in seen:
            continue
        if not grid[i][j]:
            continue
        region_count += 1
        dfs(i, j)
print(region_count)
