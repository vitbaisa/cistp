#!/usr/bin/python3

import sys
import copy
from decimal import *

class Node():
    def __init__(self, word="", matrix={}, sumc=0.0, center=0.0):
        self.word = word#.split("-", 1)[0]
        self.matrix = matrix
        self.children = []
        self.parent = None
        self.depth = 1
        self.center = center
        if sumc:
            for k in self.matrix:
                self.matrix[k] = Decimal(self.matrix[k]) / sumc # normalize values

    def __add__(self, other):
        new = Node()
        self.parent = new
        other.parent = new
        new.children = [self, other]
        new.word = "(" + self.word + " " + other.word + ")"
        new.matrix = {}
        for k1 in set(self.matrix.keys()) | set(other.matrix.keys()):
            new.matrix[k1] = (self.matrix.get(k1, Decimal(0.0)) + other.matrix.get(k1, Decimal(0.0))) / 2
        new.center = (self.center + other.center) / 2.0
        new.depth = self.depth + other.depth
        return new

    def diff(self, other):
        s = Decimal(0.0)
        c1_items = self.matrix.keys()
        c2_items = other.matrix.keys()
        for k in set(c1_items) | set(c2_items):
            v1 = self.matrix.get(k, Decimal(0.0))
            v2 = other.matrix.get(k, Decimal(0.0))
            s += abs(v1 - v2)
        return s# / len(set(c1_items) | set(c2_items))


if __name__ == "__main__":
    wl = []
    for line in open(sys.argv[1]):
        w = line.strip()
        if w:
            wl.append(w)

    data = {}
    linec = 0
    too_large = 0
    sumc_d = {}

    for line in sys.stdin:
        linec += 1
        count, w, senlen, pos = line.strip().split('\t')
        count = int(count)
        senlen = int(senlen)
        pos = int(pos)
        if pos > 255 or senlen > 255:
            too_large += 1
            continue
        data.setdefault(w, {}).setdefault((pos, senlen), 0)
        data[w][(pos, senlen)] += count
        sumc_d.setdefault(w, 0)
        sumc_d[w] += count

    #print("Line processed: %d" % linec, file=sys.stderr)
    #print("Datapoints omitted: %d" % too_large, file=sys.stderr)

    if '--draw' in sys.argv:
        from PIL import Image
        for w in data:
            if w in wl:
                print("Image: ", w, file=sys.stderr)
                img = Image.new('RGB', (100, 100), "white")
                pixels = img.load()
                for (pos, senlen) in data[w]:
                    #c = 240 - (int(240 * data[w][(pos, senlen)] / float(data_sumc[w])))
                    pixels[senlen-1, 100-pos+1] = (c, c, c)
                img.save('pngs/' + w + '.png')

    # clustering
    clusters = [Node(word=x, matrix=copy.deepcopy(data[x]), sumc=sumc_d[x], center=float(i)) for i, x in enumerate(wl)]
    similarities = []
    max_score = 0.0

    cf = open(sys.argv[2] + ".txt", "w")

    for i1 in range(len(clusters)-1):
        cl1 = clusters[i1]
        for i2 in range(i1+1, len(clusters)):
            cl2 = clusters[i2]
            sc = cl1.diff(cl2)
            max_score = max(sc, max_score)
            similarities.append((sc, cl1, cl2))
    similarities.sort(reverse=True)
    for sim in similarities:
        print("SIM", sim[0], sim[1].word, sim[2].word, file=cf)

    while len(similarities) > 1:
        sc, c1, c2 = similarities.pop()
        i = 0
        while i < len(clusters):
            if clusters[i] is c1:
                break
            i += 1
        clusters.pop(i)
        i = 0
        while i < len(clusters):
            if clusters[i] is c2:
                break
            i += 1
        clusters.pop(i)
        i = 0
        while i < len(similarities):
            if similarities[i][1] is c1 or similarities[i][2] is c1:
                similarities.pop(i)
                continue
            if similarities[i][2] is c2 or similarities[i][1] is c2:
                similarities.pop(i)
                continue
            i += 1
        new = c1 + c2 # merge clusters
        #print("A", new.word, sc, file=cf)
        for cl in clusters:
            score = new.diff(cl)
            max_score = max(score, max_score)
            similarities.append((score, cl, new))
        similarities.sort(reverse=True)
        clusters.append(new)
    sc, c1, c2 = similarities.pop()
    top = c1 + c2

    newwl = top.word.replace('(', '').replace(')', '').strip().split()
    #print("JOINED CLUSTERS", top.word, file=sys.stderr)
    #print("NEW", newwl, file=sys.stderr)

    # clustering again
    clusters = [Node(word=x, matrix=copy.deepcopy(data[x]), sumc=sumc_d[x], center=float(i)) for i, x in enumerate(newwl)]
    similarities = []
    max_score = 0.0

    for i1 in range(len(clusters)-1):
        cl1 = clusters[i1]
        for i2 in range(i1+1, len(clusters)):
            cl2 = clusters[i2]
            sc = cl1.diff(cl2)
            max_score = max(sc, max_score)
            similarities.append((sc, cl1, cl2))
    similarities.sort(reverse=True)
    #for sim in similarities[-20:]:
    #    print("SIM B", sim[0], sim[1].word, sim[2].word, file=cf)

    while len(similarities) > 1:
        sc, c1, c2 = similarities.pop()
        i = 0
        while i < len(clusters):
            if clusters[i] is c1:
                break
            i += 1
        clusters.pop(i)
        i = 0
        while i < len(clusters):
            if clusters[i] is c2:
                break
            i += 1
        clusters.pop(i)
        i = 0
        while i < len(similarities):
            if similarities[i][1] is c1 or similarities[i][2] is c1:
                similarities.pop(i)
                continue
            if similarities[i][2] is c2 or similarities[i][1] is c2:
                similarities.pop(i)
                continue
            i += 1
        new = c1 + c2 # merge clusters
        #print("B", new.word, sc, file=cf)
        for cl in clusters:
            score = new.diff(cl)
            max_score = max(score, max_score)
            similarities.append((score, cl, new))
        similarities.sort(reverse=True)
        clusters.append(new)
    sc, c1, c2 = similarities.pop()
    top = c1 + c2

    #print("JOINED CLUSTERS", top.word, file=sys.stderr)

    width = 4800
    height = 4800

    stack = [top]
    max_depth = top.depth

    svgf = open(sys.argv[2] + '.svg', "w")
    print('<svg width="%d" height="%d">' % (width, height), file=svgf)
    hstep = width / top.depth
    vstep = height / len(wl)

    while stack:
        top = stack.pop()
        if top.children:
            centers = []
            for child in reversed(top.children):
                centers.append(child.center)
                print('  <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="green" stroke-width="2" />' %\
                        (hstep * (max_depth - top.depth), vstep * child.center, hstep * (max_depth-child.depth), vstep * child.center), file=svgf)
                stack.append(child)
            print('  <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="red" stroke-width="2" />' %\
                    (hstep * (max_depth-top.depth), vstep * centers[0], hstep * (max_depth-top.depth), vstep * centers[1]), file=svgf)
        else:
            print('  <text x="%d" y="%d" fill="black">%s</text>' %\
                    (width, vstep * top.center, top.word), file=svgf)
    print('</svg>', file=svgf)
    svgf.close()
