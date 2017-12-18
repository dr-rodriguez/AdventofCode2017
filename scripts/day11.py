"""
--- Day 11: Hex Ed ---
Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you,
clearly in distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north,
northeast, southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \
You have the path the child process took. Starting where he started, you need to determine the fewest
number of steps required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)

For example:

ne,ne,ne is 3 steps away.
ne,ne,sw,sw is 0 steps away (back where you started).
ne,ne,s,s is 2 steps away (se,se).
se,sw,se,sw,sw is 3 steps away (s,s,sw).
"""

"""My notes
n+s = 0, e+w=0
ne+sw = 0, nw+se = 0
ne+nw = n, se+sw = s
"""

from collections import Counter

with open('data/day11.txt', 'r') as f:
    raw_data = f.read().rstrip().split(',')

my_input = Counter(raw_data)
my_input

# NE -> NW = N
my_input['ne'] -= my_input['nw']
my_input['n'] += my_input['nw']
my_input['nw'] = 0

# SE -> SW = S
my_input['se'] -= my_input['sw']
my_input['s'] += my_input['sw']
my_input['sw'] = 0

# NE -> S = SE
my_input['s'] -= my_input['ne']
my_input['se'] += my_input['ne']
my_input['ne'] = 0

# N -> S = 0
my_input['n'] = my_input['n'] - my_input['s']
my_input['s'] = 0

# N -> SE = NE
my_input['se'] -= my_input['n']
my_input['ne'] += my_input['n']
my_input['n'] = 0

steps = 0
for k, v in my_input.items():
    steps += v
print(steps)

# 53 is incorrect
# 337 is too low
# 942 is too high

"""
--- Part Two ---
How many steps away is the furthest he ever got from his starting position?
"""


