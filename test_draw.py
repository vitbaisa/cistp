#!/usr/bin/python3

import copy

def get_list(c):
    if type(c[0]) == type(()) and type(c[1]) == type(()):
        return get_list(c[0]) + get_list(c[1])
    elif type(c[0]) == type("") and type(c[1]) == type(()):
        return [(c[0], c[2])] + get_list(c[1])
    elif type(c[1]) == type("") and type(c[0]) == type(()):
        return get_list(c[0]) + [(c[1], c[2])]
    elif type(c[0]) == type("") and type(c[1]) == type(""):
        return [(c[0], c[2]), (c[1], c[2])]
    else:
        raise Exception("What???")

clusters = [(((("a", "b", 1.5), "c", 1.7), "d", 1.9), (("e", "f", 1.3), "g", 1.9), 2.1)]
leaves = get_list(clusters[0])
max_score = max(map(lambda x: x[1], leaves))

stack = [clusters[0]]
postack = [[0, 0]]

width = 1000
height = 1000
line_height = float(height) / len(leaves)

print('<svg width="%d" height="%d">' % (width, height))
counter = 0
RLINE = ' <line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke: red;" />'
BLINE = ' <line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke: blue;" />'
GLINE = ' <line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke: green;" />'
PLINE = ' <line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke: purple;" />'
TEXT = ' <text x="%d" y="%d" fill="black">%s</text>'

while stack:
    top = copy.deepcopy(stack.pop())
    if type(top[0]) == type(()) and type(top[1]) == type(()):
        stack.append(top[1])
        stack.append(top[0])
    elif type(top[0]) == type(""):
        sc = top[2]
        print(TEXT % (width-width*(sc/max_score), counter*line_height, top[0]))
        print(GLINE % (width-width*(sc/max_score), counter*line_height, width, counter*line_height))
        counter += 1
        if type(top[1]) == type(""):
            sc = top[2]
            print(TEXT % (width-width*(sc/max_score), counter*line_height, top[1]))
            print(GLINE % (width-width*(sc/max_score), counter*line_height, width, counter*line_height))
            counter += 1
        elif type(top[1]) == type(()):
            stack.append(top[1])
    elif type(top[1]) == type(""):


print('</svg>')
