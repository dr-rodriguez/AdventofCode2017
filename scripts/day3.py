"""
--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and
then counting up while spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...
While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1
(the location of the only access port for this memory system) by programs that can only move up, down, left, or right.
They always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.
How many steps are required to carry the data from the square
identified in your puzzle input all the way to the access port?

Your puzzle input is 277678.
"""

# NOTES that might be useful
# Bottom right of each spiral level is 1, 9 (3^2), 25 (5^2), 49 (7^2), ...
# For first level, (3^2=9), corners are 9, 7, 5, 3 (-2 each)
# For second level (5^2=25), corners are 25, 21, 17, 13 (-4 each)
# Corners need an extra move
# There are 8 values in lvl 1, 16 (8*2) in lvl 2, 24 (8*3) in lvl 3, ...
# Going right, up, left, bottom means adding to the number (9, 11, 13, 15), (17, 19, 21, 23)
# This is lvl*8+1 and then +2 for each subsequent direction
# Level : Factor : Factor^2 = 1:3:9, 2:5:25, 3:7:49

"""
37  36  35  34  33  32  31
38  17  16  15  14  13  30
39  18   5   4   3  12  29
40  19   6   1   2  11  28
41  20   7   8   9  10  27
42  21  22  23  24  25  26
43  44  45  46  47  48  49
"""

import math
import numpy as np


def get_corners(num):
    return np.array([num**2 - i*(num-1) for i in range(4)])


def get_level(val):
    temp = math.ceil(math.sqrt(val))
    if temp % 2 == 0:  # even numbers promote to odd
        temp += 1
    return temp//2


def get_direction(val):
    global moves
    lvl = get_level(val)
    corners = get_corners(lvl*2 + 1)
    # Check if corner
    ind, = np.where(val == corners)
    if len(ind) > 0:
        print('{} is corner'.format(val))
        moves += 1
        val -= 1
    ind, = np.where(val <= corners)
    # 0=bottom, 1=left, 2=top, 3=right
    return max(ind), val


def move_lvl(val):
    global moves
    # Going right, up, left, bottom means adding to the number (9, 11, 13, 15), (17, 19, 21, 23)
    # This is lvl*8+1 and then +2 for each subsequent direction
    lvl = get_level(val) - 1  # go down 1 level
    offset = [lvl*8+1 + 2*i for i in range(4)]  # right, top, left, bottom
    offset = offset[::-1]  # 0=bottom, 1=left, 2=top, 3=right
    dir, val = get_direction(val)
    my_offset = offset[dir]
    print(val, lvl, offset, dir, my_offset)
    newval = val - my_offset
    moves += 1
    return newval


val = 277678
moves = 0
while val != 1:
    print(moves, val)
    val = move_lvl(val)
print(moves, val)

"""
--- Part Two ---

As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1.
Then, in the same allocation order as shown above, they store the sum of the values in all adjacent squares,
including diagonals.

So, the first few squares' values are chosen as follows:

Square 1 starts with the value 1.
Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.
Once a square is written, its value does not change.
Therefore, the first few squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...

What is the first value written that is larger than your puzzle input?
"""

# NOTES that might be useful
# This feels like some twisted fibonacci sequence
# This implies the first part may have been easier just generating the spiral itself

# i  x  y val
# 0  0  0 1
# 1  1  0 1
# 2  1  1 2
# 3  0  1 4
# 4 -1  1 5
# 5 -1  0 10
# 6 -1 -1 11
# 7  0 -1 23
# 8  1 -1 25
# 9  2 -1 26


def get_newvalue(loc):
    global grid
    x, y = loc[0], loc[1]
    sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            sum += grid.get((x+i, y+j), 0)
    grid[loc] = sum
    return sum

# Lvl : max up    = 1:1, 2:3, 3:5
# Lvl : max left  = 1:2, 2:4, 3:6
# Lvl : max down  = 1:2, 2:4, 3:6
# Lvl : max right = 1:2, 2:4, 3:6
def get_newloc(loc, verbose=False):
    global lvl
    global counts
    maxup = lvl*2 - 1
    maxleft, maxdown, maxright = lvl*2, lvl*2, lvl*2
    x, y = loc[0], loc[1]
    # up, left, down, right
    if counts[0] < maxup:
        if verbose: print('up')
        loc = (x, y+1)
        val = get_newvalue(loc)
        counts[0] += 1
    elif counts[1] < maxleft:
        if verbose: print('left')
        loc = (x-1, y)
        val = get_newvalue(loc)
        counts[1] += 1
    elif counts[2] < maxdown:
        if verbose: print('down')
        loc = (x, y-1)
        val = get_newvalue(loc)
        counts[2] += 1
    elif counts[3] < maxright:
        if verbose: print('right')
        loc = (x+1, y)
        val = get_newvalue(loc)
        counts[3] += 1
    else:  # move to next level
        if verbose: print('lvl up')
        loc = (x + 1, y)
        lvl += 1
        val = get_newvalue(loc)
        counts = [0, 0, 0, 0]
    return loc, val

counts = [0, 0, 0, 0]
lvl = 1
grid = {(0,0):1, (1,0):1}
loc = (1,0)
val = 1
while val <= 277678:
    print(loc, val)
    loc, val = get_newloc(loc)
print(loc, val)
