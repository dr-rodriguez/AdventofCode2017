"""
--- Day 23: Coprocessor Conflagration ---
You decide to head directly to the CPU and fix the printer from there.
As you get close, you find an experimental coprocessor doing so much work that the local
programs are afraid it will halt and catch fire. This would cause serious issues for the rest of the computer,
so you head in and see what you can do.

The code it's running seems to be a variant of the kind you saw recently on that tablet.
The general functionality seems very similar, but some of the instructions are different:

set X Y sets register X to the value of Y.
sub X Y decreases register X by the value of Y.
mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero.
(An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
Only the instructions listed above are used. The eight registers here, named a through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which allows for testing,
but prevents it from doing any meaningful work.

If you run the program (your puzzle input), how many times is the mul instruction invoked?
"""


def proc_move(reg, elem, i):
    try:
        v = int(elem[2])
    except ValueError:
        v = reg.get(elem[2], 0)
    except IndexError:
        v = 0

    try:
        x = int(elem[1])
    except ValueError:
        x = reg.get(elem[1], 0)
    except IndexError:
        x = 0

    if elem[0] == 'set':
        reg[elem[1]] = v
    elif elem[0] == 'add':
        reg[elem[1]] = reg.get(elem[1], 0) + v
    elif elem[0] == 'sub':
        reg[elem[1]] = reg.get(elem[1], 0) - v
    elif elem[0] == 'mul':
        reg[elem[1]] = reg.get(elem[1], 0) * v
    elif elem[0] == 'mod':
        reg[elem[1]] = reg.get(elem[1], 0) % v
    elif elem[0] == 'jnz':
        if x != 0:
            i += v
            return i

    i += 1
    return i


with open('data/day23.txt', 'r') as f:
    my_input = f.read().rstrip().split('\n')

register = {}
count = 0
ind = 0
while True:
    if ind < 0 or ind >= len(my_input):
        break

    elem = my_input[ind].split(' ')
    if elem[0] == 'mul':
        count += 1

    ind = proc_move(register, elem, ind)

print(count)

"""
--- Part Two ---
Now, it's time to fix the problem.

The debug mode switch is wired directly to register a. You flip the switch,
which makes register a now start at 1 when the program is executed.

Immediately, the coprocessor begins to overheat. Whoever wrote this program obviously didn't choose
a very efficient implementation. You'll need to optimize the program if it has any hope of
completing before Santa needs that printer working.

The coprocessor's ultimate goal is to determine the final value left in register h once the program completes.
Technically, if it had that... it wouldn't even need to run the program.

After setting register a to 1, if the program were to run to completion, what value would be left in register h?
"""

register = {'a': 1}
ind = 0
count = 0
while True:
    if ind < 0 or ind >= len(my_input):
        break

    elem = my_input[ind].split(' ')
    ind = proc_move(register, elem, ind)
    # print(elem)
    # print(register)
    count += 1
    # if count > 10000:
    #     break

print(register.get('h'))
# Need to examine what the code is doing and see if I see a pattern

count = 4113968717
ind = 17
register = {'c': 126900, 'b': 109900, 'd': 4681, 'f': 0, 'e': 33107, 'g': -76793, 'a': 1}

count = 9318296915
ind = 19
register = {'c': 126900, 'b': 109900, 'd': 10600, 'f': 0, 'e': 84170, 'g': -25730, 'a': 1}
