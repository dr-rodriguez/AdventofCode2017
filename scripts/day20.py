"""
--- Day 20: Particle Swarm ---
Suddenly, the GPU contacts you, asking for help. Someone has asked it to simulate too many particles,
and it won't be able to finish them all in time to render the next frame at this rate.

It transmits to you a buffer (your puzzle input) listing each particle in order (starting with particle 0,
then particle 1, particle 2, and so on). For each particle, it provides the X, Y,
and Z coordinates for the particle's position (p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.

Each tick, all particles are updated simultaneously. A particle's properties are updated in the following order:

Increase the X velocity by the X acceleration.
Increase the Y velocity by the Y acceleration.
Increase the Z velocity by the Z acceleration.
Increase the X position by the X velocity.
Increase the Y position by the Y velocity.
Increase the Z position by the Z velocity.
Because of seemingly tenuous rationale involving z-buffering,
the GPU would like to know which particle will stay closest to position <0,0,0> in the long term.
Measure this using the Manhattan distance,
which in this situation is simply the sum of the absolute values of a particle's X, Y, and Z position.

For example, suppose you are only given two particles, both of which stay entirely on the X-axis (for simplicity).
Drawing the current states of particles 0 and 1 (in that order)
with an adjacent a number line and diagram of current X positions (marked in parenthesis),
the following would take place:

p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)

p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)

p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)

p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)
At this point, particle 1 will never be closer to <0,0,0> than particle 0, and so,
in the long run, particle 0 will stay closest.

Which particle will stay closest to position <0,0,0> in the long term?
"""

# Had to get help from Reddit since I was not getting correct answers despite my approach.
# Issues were mainly with lists/dicts/etc as well as picking closest particle as opposed to which remains closest

import re
from collections import defaultdict  # defaultdict appends to existing elements

test_input = """p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>"""
my_input = test_input.split('\n')

with open('data/day20.txt', 'r') as f:
    my_input = f.read().rstrip().split('\n')


class Particle:
    def __init__(self, vec):
        self.p = vec[0:3]
        self.v = vec[3:6]
        self.a = vec[6:9]
        self.present = True

    def step(self):
        for i in range(3):
            self.v[i] += self.a[i]
            self.p[i] += self.v[i]

    def get_d(self):
        return sum([abs(s) for s in self.p])

pattern = r'p=<([ \-\d]*),([ \-\d]*),([ \-\d]*)>, v=<([ \-\d]*),([ \-\d]*),([ \-\d]*)>, a=<([ \-\d]*),([ \-\d]*),([ \-\d]*)>'
particles = []
for i, line in enumerate(my_input):
    t = re.findall(pattern, line)[0]
    particles.append(Particle([int(s) for s in t]))

count = 0
while True:
    closev = None
    closek = None
    for i, part in enumerate(particles):
        part.step()
        d = part.get_d()
        if closev is None or d < closev:
            closek = i
            closev = d

    print(closek, closev)
    count += 1
    if count >= 1000:
        break

print(closek, closev)
# 389 reaches 4, the closest location, but after a while the particle that remains closest (though never as close) is 91

"""
--- Part Two ---
To simplify the problem further, the GPU would like to remove any particles that collide.
Particles collide if their positions ever exactly match.
Because particles are updated simultaneously, more than two particles can collide at the same time and place.
Once particles collide, they are removed and cannot collide with anything else after that tick.

For example:

p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>    (0)   (1)   (2)            (3)
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=<-3,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-1,0,0>, v=< 1,0,0>, a=< 0,0,0>             (0)(1)(2)      (3)
p=< 2,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=< 0,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=< 0,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=< 0,0,0>, v=< 1,0,0>, a=< 0,0,0>                       X (3)
p=< 1,0,0>, v=<-1,0,0>, a=< 0,0,0>

------destroyed by collision------
------destroyed by collision------    -6 -5 -4 -3 -2 -1  0  1  2  3
------destroyed by collision------                      (3)
p=< 0,0,0>, v=<-1,0,0>, a=< 0,0,0>
In this example, particles 0, 1, and 2 are simultaneously destroyed at the time and place marked X.
On the next tick, particle 3 passes through unharmed.

How many particles are left after all collisions are resolved?
"""

# Need to convert to dict as otherwise removing from list changes numbers
part_dict = {}
for i, k in enumerate(particles):
    part_dict[i] = k

count = 0
while True:
    plist = defaultdict(list)
    for i, part in part_dict.items():
        part.step()
        plist[tuple(part.p)].append(i)

    # Check for collisions
    for k, v in plist.items():
        if len(v) > 1:
            print(k, v)
            for j in v:
                del part_dict[j]

    count += 1
    if count >= 1000:
        break

print(len(part_dict))


