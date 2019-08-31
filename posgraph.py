#!/usr/bin/python3

import sys
from PIL import Image

data = {}
maxl = 0
maxc = 0

for line in sys.stdin:
    count, item, senlen, pos = line.strip().split('\t')
    count = int(count)
    senlen = int(senlen)
    pos = int(pos)
    data.setdefault((pos, senlen), 0)
    data[(pos, senlen)] += count
    if maxl < senlen:
        maxl = senlen
    if maxc < count:
        maxc = count

print('MAX COUNT', maxc)
print('MAX LEN', maxl)

img = Image.new('RGB', (maxl+1, maxl+1), "white")
pixels = img.load()

for item in data:
    c = 240 - (int(200 * (data[item] / float(maxc))))
    pixels[item[1]-1, maxl-item[0]+1] = (c, c, c)

if len(sys.argv) > 1:
    fn = sys.argv[1]
else:
    fn = 'output.png'

img.save(fn)
