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
# Simulating this takes an eternity!
# Working it out by hand:
"""
a = 1
b = 9900 + 100000 = 109900
c = b + 17000 = 126900

f = 1
{
    d = 2
    {
        e = 2
        {
            g = (d * e) - b
            if g == 0: (or: d*e == b)
                f = 0
            e += 1
            g = e - b
            if e == b: break from this loop
        }
        d += 1
        g = d - b
        if d == b: break from this loop
    }
    if f == 0:
        h += 1  # most important step
    g = b - c
    if b == c:
        break from this loop
    else:
        b = b + 17
        f = 1
        continue the outer-most loop
}

set f 1 ...<
set d 2
set e 2 <<<
set g d <<
mul g e
sub g b
jnz g 2 >
set f 0
sub e -1 <
set g e
sub g b
jnz g -8 >>
sub d -1
set g d
sub g b
jnz g -13 >>>
jnz f 2 >.
sub h -1
set g b .<
sub g c
jnz g 2 >..
jnz 1 3 EOF
sub b -17 ..<
jnz 1 -23 >...
"""

a = 1
b = 109900
c = b + 17000
h = 0
# for b in range(109900, c+1, 17):  # c+1 to include last case (b=c)
#     f = 1
#     for d in range(2, b):
#         if f == 0: continue  # if already found to be prime, no need to continue
#         for e in range(2, b):
#             if d * e == b:  # if not prime, set to 0
#                 f = 0
#                 break
#     if f == 0:
#         h += 1
#         print(b, c, h)
# print(h)
# This still takes too long since it's so many loops.

# Function from stack overflow to check if prime
import math
def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0 or n <= 1:
        return False

    sqr = int(math.sqrt(n)) + 1

    for divisor in range(3, sqr, 2):
        if n % divisor == 0:
            return False
    return True


for b in range(109900, c+1, 17):  # c+1 to include last case (b=c)
    if not is_prime(b):
        h += 1
        print(b, c, h)
print('DONE')
print(h)
