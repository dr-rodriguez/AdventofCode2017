"""
--- Day 21: Fractal Art ---
You find a program trying to generate some art.
It uses a strange process that involves repeatedly enhancing the detail of an image through a set of rules.

The image consists of a two-dimensional square grid of pixels that are either on (#) or off (.).
The program always begins with this pattern:

.#.
..#
###
Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have a size of 3.

Then, the program repeats the following process:

If the size is evenly divisible by 2, break the pixels up into 2x2 squares, and convert each 2x2 square
into a 3x3 square by following the corresponding enhancement rule.
Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3 squares, and convert each 3x3
square into a 4x4 square by following the corresponding enhancement rule.
Because each square of pixels is replaced by a larger one, the image gains pixels and so its size increases.

The artist's book of enhancement rules is nearby (your puzzle input); however, it seems to be missing rules.
The artist explains that sometimes, one must rotate or flip the input pattern to find a match.
(Never rotate or flip the output pattern, though.) Each pattern is written concisely: rows are listed as single units,
ordered top-down, and separated by slashes. For example, the following rules correspond to the adjacent patterns:

../.#  =  ..
          .#

                .#.
.#./..#/###  =  ..#
                ###

                        #..#
#..#/..../#..#/.##.  =  ....
                        #..#
                        .##.
When searching for a rule to use, rotate and flip the pattern as necessary.
For example, all of the following patterns match the same rule:

.#.   .#.   #..   ###
..#   #..   #.#   ..#
###   ###   ##.   .#.
Suppose the book contained the following two rules:

../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
As before, the program begins with this pattern:

.#.
..#
###
The size of the grid (3) is not divisible by 2, but it is divisible by 3.
It divides evenly into a single square; the square matches the second rule, which produces:

#..#
....
....
#..#
The size of this enhanced grid (4) is evenly divisible by 2, so that rule is used.
It divides evenly into four squares:

#.|.#
..|..
--+--
..|..
#.|.#
Each of these squares matches the same rule (../.# => ##./#../...),
three of which require some flipping and rotation to line up with the rule.
The output for the rule is the same in all four cases:

##.|##.
#..|#..
...|...
---+---
##.|##.
#..|#..
...|...
Finally, the squares are joined into a new grid:

##.##.
#..#..
......
##.##.
#..#..
......
Thus, after 2 iterations, the grid contains 12 pixels that are on.

How many pixels stay on after 5 iterations?
"""

import numpy as np
import re

def matrixfy(str):
    """Create and return matrix given string"""
    temp = []
    for line in str.split('/'):
        temp.append([s for s in line])
    return np.array(temp)


def dematrixfy(mat):
    """Create string from matrix"""
    return '/'.join([''.join(ss) for ss in mat])

with open('data/day21.txt', 'r') as f:
    rawrules = f.read().split('\n')

rules = {}
for line in rawrules:
    k, v = re.findall(r'([\w\.\#\/]*) => ([\w\.\#\/]*)', line.strip())[0]
    rules[k] = v

# Populate rules with rotated and flipped versions
# np.rot90  # rotate by 90 deg
# np.fliplr , np.flipup  flip left/right and up/down
# Rotations
newrules = {}
for k, v in rules.items():
    kmat = matrixfy(k)
    for i in range(1, 4):
        kmat2 = dematrixfy(np.rot90(kmat, i))
        if kmat2 not in rules.keys():
            newrules[kmat2] = v
for k, v in newrules.items():
    rules[k] = v
# Flips
newrules = {}
for k, v in rules.items():
    kmat = matrixfy(k)
    kmat2 = dematrixfy(np.fliplr(kmat))
    if kmat2 not in rules.keys():
        newrules[kmat2] = v
    kmat2 = dematrixfy(np.flipud(kmat))
    if kmat2 not in rules.keys():
        newrules[kmat2] = v
for k, v in newrules.items():
    rules[k] = v

pattern = np.array([['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']])
for ii in range(5):
    lenpat = len(pattern)
    if lenpat % 2 == 0:
        nextpattern = np.array(np.array([[s for s in '.' * (lenpat + lenpat // 2)]] * (lenpat + lenpat // 2)))
        # Divisible by 2
        for i in range(lenpat // 2):
            for j in range(lenpat // 2):
                subpat = dematrixfy(pattern[i * 2:(i + 1) * 2, j * 2:(j + 1) * 2])
                newpat = matrixfy(rules[subpat])
                nextpattern[i * 3:(i + 1) * 3, j * 3:(j + 1) * 3] = newpat
    elif lenpat % 3 == 0:
        nextpattern = np.array(np.array([[s for s in '.' * (lenpat + lenpat//3)]] * (lenpat + lenpat//3)))
        # Divisible by 3
        for i in range(lenpat//3):
            for j in range(lenpat//3):
                subpat = dematrixfy(pattern[i*3:(i+1)*3, j*3:(j+1)*3])
                newpat = matrixfy(rules[subpat])
                nextpattern[i*4:(i+1)*4, j*4:(j+1)*4] = newpat
    else:
        break

    pattern = nextpattern
    print(ii, '{} -> {}'.format(lenpat, len(pattern)))

unique, counts = np.unique(pattern, return_counts=True)
ans = dict(zip(unique, counts))
print(ans['#'])


"""
--- Part Two ---

How many pixels stay on after 18 iterations?
"""

# Brute forcing it works fine (takes a few seconds)

pattern = np.array([['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']])
for ii in range(18):
    lenpat = len(pattern)
    if lenpat % 2 == 0:
        nextpattern = np.array(np.array([[s for s in '.' * (lenpat + lenpat // 2)]] * (lenpat + lenpat // 2)))
        # Divisible by 2
        for i in range(lenpat // 2):
            for j in range(lenpat // 2):
                subpat = dematrixfy(pattern[i * 2:(i + 1) * 2, j * 2:(j + 1) * 2])
                newpat = matrixfy(rules[subpat])
                nextpattern[i * 3:(i + 1) * 3, j * 3:(j + 1) * 3] = newpat
    elif lenpat % 3 == 0:
        nextpattern = np.array(np.array([[s for s in '.' * (lenpat + lenpat//3)]] * (lenpat + lenpat//3)))
        # Divisible by 3
        for i in range(lenpat//3):
            for j in range(lenpat//3):
                subpat = dematrixfy(pattern[i*3:(i+1)*3, j*3:(j+1)*3])
                newpat = matrixfy(rules[subpat])
                nextpattern[i*4:(i+1)*4, j*4:(j+1)*4] = newpat
    else:
        break

    pattern = nextpattern
    print(ii, '{} -> {}'.format(lenpat, len(pattern)))

unique, counts = np.unique(pattern, return_counts=True)
ans = dict(zip(unique, counts))
print(ans['#'])
