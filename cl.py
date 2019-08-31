import sys
import glob

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        s = []
        for line in f:
            _, sim, lempos1, lempos2 = line.rstrip('\n').split()
            s.append((float(sim), lempos1, lempos2))
        s.sort()
        out = set()
        for s, l1, l2 in s:
            if not l1 in out:
                print(l1, l2, s)
                out.add(l1)
