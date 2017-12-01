"""
--- Day 1: Inverse Captcha ---

The night before Christmas, one of Santa's Elves calls you in a panic.
"The printer's broken! We can't print the Naughty or Nice List!"
By the time you make it to sub-basement 17, there are only a few minutes until midnight.
"We have a big problem," she says; "there must be almost fifty bugs in this system,
but nothing else can print The List. Stand in this square, quick!
There's no time to explain; if you can convince them to pay you in stars, you'll be able to--"
She pulls a lever and the world goes blurry.

When your eyes can focus again, everything seems a lot more pixelated than before.
She must have sent you inside the computer! You check the system clock: 25 milliseconds until midnight.
With that much time, you should be able to collect all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day
millisecond in the advent calendar; the second puzzle is unlocked when you complete the first.
Each puzzle grants one star. Good luck!

You're standing in a room with "digitization quarantine" written in LEDs along one wall.
The only door is locked, but it includes a small interface. "Restricted Area - Strictly No Digitized Users Allowed."

It goes on to explain that you may only leave by solving a captcha to prove you're not a human.
Apparently, you only get one millisecond to solve the captcha: too fast for a normal human,
 but it feels like hours to you.

The captcha requires you to review a sequence of digits (your puzzle input) and find the sum
of all digits that match the next digit in the list. The list is circular,
so the digit after the last digit is the first digit in the list.

For example:

1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the second digit
and the third digit (2) matches the fourth digit.
1111 produces 4 because each digit (all 1) matches the next.
1234 produces 0 because no digit matches the next.
91212129 produces 9 because the only digit that matches the next one is the last digit, 9.
What is the solution to your captcha?
"""

import re

mine = '29917128875332952564321392569634257121244516819997569284938677239676779378822158323549832814412597817651244117851771257438674567254146559419528411463781241159837576747416543451994579655175322397355255587935456185669334559882554936642122347526466965746273596321419312386992922582836979771421518356285534285825212798113159911272923448284681544657616654285632235958355867722479252256292311384799669645293812691169936746744856227797779513997329663235176153745581296191298956836998758194274865327383988992499115472925731787228592624911829221985925935268785757854569131538763133427434848767475989173579655375125972435359317237712667658828722623837448758528395981635746922144957695238318954845799697142491972626942976788997427135797297649149849739186827185775786254552866371729489943881272817466129271912247236569141713377483469323737384967871876982476485658337183881519295728697121462266226452265259877781881868585356333494916519693683238733823362353424927852348119426673294798416314637799636344448941782774113142925315947664869341363354235389597893211532745789957591898692253157726576488811769461354938575527273474399545366389515353657644736458182565245181653996192644851687269744491856672563885457872883368415631469696994757636288575816146927747179133188841148212825453859269643736199836818121559198563122442483528316837885842696283932779475955796132242682934853291737434482287486978566652161245555856779844813283979453489221189332412315117573259531352875384444264457373153263878999332444178577127433891164266387721116357278222665798584824336957648454426665495982221179382794158366894875864761266695773155813823291684611617853255857774422185987921219618596814446229556938354417164971795294741898631698578989231245376826359179266783767935932788845143542293569863998773276365886375624694329228686284863341465994571635379257258559894197638117333711626435669415976255967412994139131385751822134927578932521461677534945328228131973291962134523589491173343648964449149716696761218423314765168285342711137126239639867897341514131244859826663281981251614843274762372382114258543828157464392'


def sum_captcha(val, sum=0):
    pattern = r'(\d)\1'
    groups = re.findall(pattern, val)
    if len(groups) == 0:
        return sum
    else:
        g = groups[0]
        newval = re.sub(g+g, g, val, 1)
        return sum_captcha(newval, sum + int(g))


# val = '1122'
# val = '1111'
# val = '1234'
# val = '91212129'
# sum_captcha(val + val[0])

ans = sum_captcha(mine+mine[0])
print('Part 1: {}'.format(ans))

"""
--- Part Two ---

You notice a progress bar that jumps to 50% completion. 
Apparently, the door isn't yet satisfied, but it did emit a star as encouragement. The instructions change:

Now, instead of considering the next digit, it wants you to consider the digit halfway around the circular list. 
That is, if your list contains 10 items, only include a digit in your sum if the digit 10/2 = 5 
steps forward matches it. Fortunately, your list has an even number of elements.

For example:

1212 produces 6: the list contains 4 items, and all four digits match the digit 2 items ahead.
1221 produces 0, because every comparison is between a 1 and a 2.
123425 produces 4, because both 2s match each other, but no other digit has a match.
123123 produces 12.
12131415 produces 4.
What is the solution to your new captcha?
"""


def sum_captcha2(val):
    length = len(val)
    offset = int(length/2)
    sum = 0
    for ind, v in enumerate(val):
        # print(ind, v, val[(ind + offset) % length])
        if v == val[(ind + offset) % length]:
            sum += int(v)
    return sum


# val = '1212'
# val = '1221'
# val = '123425'
# val = '123123'
# val = '12131415'
# sum_captcha2(val)

ans = sum_captcha2(mine)
print('Part 2: {}'.format(ans))
