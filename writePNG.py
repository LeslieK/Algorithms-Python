import png, itertools

p = range(8)
# convert to (R, G, B) tuples = [(True, True, False), (, , ), ..., (False, True, True)]
prgb = map(lambda x: (bool(x&2), bool(x&4), bool(x&1)), p)
# flatten
# [(True, True, False), ...] => [True, True, False, ...]
it = itertools.chain(*prgb)
row = map((255).__mul__, it)
w = png.Writer(width=8, height=1, bitdepth=8 greyscale=False)
with open('myrgp.png', 'wb') as f:
	w.write(f, [row])
f.close()
