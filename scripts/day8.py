"""
--- Day 8: I Heard You Like Registers ---

You receive a signal directly from the CPU. Because of your recent assistance with jump instructions,
it would like you to compute the result of a series of unusual register instructions.

Each instruction consists of several parts: the register to modify, whether to increase or decrease that
register's value, the amount by which to increase or decrease it, and a condition.
If the condition fails, skip the instruction without modifying the register.
The registers all start at 0. The instructions look like this:

b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
These instructions would be processed as follows:

Because a starts at 0, it is not greater than 1, and so b is not modified.
a is increased by 1 (to 1) because b is less than 5 (it is 0).
c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
c is increased by -20 (to -10) because c is equal to 10.
After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to).
However, the CPU doesn't have the bandwidth to tell you what all the registers are named,
and leaves that to you to determine.

What is the largest value in any register after completing the instructions in your puzzle input?
"""

test_input = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
my_input = test_input.split('\n')

with open('data/day8.txt', 'r') as f:
    my_input = f.read().split('\n')
my_input = [s.strip() for s in my_input]


def check_condition(reg, cond, check):
    global registers
    ans = False
    if cond == '>':
        ans = registers.get(reg, 0) > check
    elif cond == '>=':
        ans = registers.get(reg, 0) >= check
    elif cond == '<':
        ans = registers.get(reg, 0) < check
    elif cond == '<=':
        ans = registers.get(reg, 0) <= check
    elif cond == '==':
        ans = registers.get(reg, 0) == check
    elif cond == '!=':
        ans = registers.get(reg, 0) != check
    return ans

registers = {}
for line in my_input:
    elems = line.split()
    reg1 = elems[0]
    fac = 1 if elems[1] == 'inc' else -1
    step = int(elems[2])
    reg2 = elems[4]
    cond = elems[5]
    check = int(elems[6])
    go = check_condition(reg2, cond, check)
    if go:
        registers[reg1] = registers.get(reg1, 0) + fac*step

print(max(registers.values()))

"""
--- Part Two ---

To be safe, the CPU also needs to know the highest value held in any register during this process
so that it can decide how much memory to allocate to these operations.
For example, in the above instructions, the highest value ever held was 10
(in register c after the third instruction was evaluated).
"""

registers = {}
maximum = 0
for line in my_input:
    elems = line.split()
    reg1 = elems[0]
    fac = 1 if elems[1] == 'inc' else -1
    step = int(elems[2])
    reg2 = elems[4]
    cond = elems[5]
    check = int(elems[6])
    go = check_condition(reg2, cond, check)
    if go:
        registers[reg1] = registers.get(reg1, 0) + fac*step
    if registers.get(reg1, 0) > maximum:
        maximum = registers.get(reg1, 0)

print(maximum)
