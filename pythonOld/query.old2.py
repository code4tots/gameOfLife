#!/usr/bin/python
# 3.28.2012
# query.py -- pairs with gameOfLife.old2.py
#
# Use gameOfLife.py to ask some questions
# about the gameOfLife.
import gameOfLife as gol

# Which arrangement gives the longest
# cycle without repeat?
R = 4
C = 4


# Build all possible values of the map.
def buildMaps(R,C):
    from itertools import product
    v = (' ', '*')

    rows = tuple(product(v,v,v,v))
    # i.e. rows ~ tuple([ tuple(x) for x in product(*([v]*C)) ])

    maps = tuple(product(rows,rows,rows,rows))
    # i.e. maps ~ [ [ list(row) for row in map ] for map in product(*([rows]*R)) ]
    
    return maps

maps = buildMaps(2,3)
print(len(maps))
print(maps[1000])
print(gol.tickImmutableModel(maps[1000]))



#for map in maps:
#    print(map)
#    break