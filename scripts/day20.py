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

import re

test_input = """p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>"""
my_input = test_input.split('\n')

with open('data/day20.txt', 'r') as f:
    my_input = f.read().rstrip().split('\n')

pattern = r'p=<([ \-\d]*),([ \-\d]*),([ \-\d]*)>, v=<([ \-\d]*),([ \-\d]*),([ \-\d]*)>, a=<([ \-\d]*),([ \-\d]*),([ \-\d]*)>'
particles = {}
for i, line in enumerate(my_input):
    t = re.findall(pattern, line)[0]
    particles[i] = [int(s) for s in t]

count = 0
closev = 9999
closek = 9999
while True:
    if count >= 1000:
        break

    for k, v in particles.items():
        # Accelerate
        vx, vy, vz = particles[k][3], particles[k][4], particles[k][5]
        ax, ay, az = particles[k][6], particles[k][7], particles[k][8]
        vx += ax
        vy += ay
        vz += az

        # Move
        particles[k][0] += vx
        particles[k][1] += vy
        particles[k][2] += vz
        particles[k][3] = vx
        particles[k][4] = vy
        particles[k][5] = vz

        # Distance
        d = sum([abs(s) for s in particles[k][0:3]])

        if d < closev:
            closek = k
            closev = d

    count += 1

print(closek, closev)
# 209 is too high
