"""
--- Day 19: A Series of Tubes ---
Somehow, a network packet got lost and ended up here. It's trying to follow a routing diagram (your puzzle input),
but it's confused about where to go.

Its starting point is just off the top of the diagram. Lines (drawn with |, -, and +) show the path it needs to take,
starting by going down onto the only line connected to the top of the diagram.
It needs to follow this path until it reaches the end (located somewhere within the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs to continue going the same direction,
and only turn left or right when there's no other option. In addition, someone has left letters on the line;
these also don't change its direction, but it can use them to keep track of where it's been. For example:

     |         .
     |  +--+   .
     A  |  C   .
 F---|----E|--+.
     |  |  |  D.
     +B-+  +--+.

Given this diagram, the packet needs to take the following path:

Starting at the only line touching the top of the diagram, it must go down, pass through A,
and continue onward to the first +.
Travel right, up, and right, passing through B in the process.
Continue down (collecting C), right, and up (collecting D).
Finally, go all the way left through E and stopping at F.
Following the path to the end, the letters it sees on its path are ABCDEF.

The little packet looks up at you, hoping you can help it find the way. What letters will it see
(in the order it would see them) if it follows the path?
(The routing diagram is very wide; make sure you view it without line wrapping.)
"""

test_input = """     |         .
     |  +--+   .
     A  |  C   .
 F---|----E|--+.
     |  |  |  D.
     +B-+  +--+."""
my_input = test_input

my_input = my_input.split('\n')
my_input = [s.split('.')[0] for s in my_input]


def proc_move(x, y, old_val, direction):
    global my_input
    val = my_input[y][x]

    if val == '|':
        if direction == 'down':
            y += 1
        else:
            y -= 1
    elif val == '-':
        if direction == 'right':
            x += 1
        else:
            x -= 1
    elif val == '+':
        if old_val == '|' or direction in ('down', 'up'):
            if direction == 'down':
                y += 1
                x1, x2 = my_input[y][x - 1, x + 1]
            else:
                y -= 1
                x1, x2 = my_input[y][x - 1, x + 1]

            if x1 != '':
                y += 1
                x -= 1
                direction = 'left'
            else:
                y += 1
                x += 1
                direction = 'right'
        elif old_val == '-' or direction in ('right', 'left'):
            if direction == 'right':
                x += 1
                y1, y2 = my_input[y - 1, y + 1][x]
            else:
                x -= 1
                y1, y2 = my_input[y - 1, y + 1][x]


    newval = my_input[y][x]

    return x, y, newval, direction

