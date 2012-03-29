#!/usr/bin/python
# gameOfLife.py (again!)

# Headers
import curses

# Global instance, GL
GL = {}

# Model (State is stored in a global instance GL)
GL['R'] = 0
GL['C'] = 0
GL['r'] = 0
GL['c'] = 0
GL['map'] = [ [' '] * GL['C'] for x in range(GL['R']) ]
GL['running'] = False
def initModel(R,C,r=0,c=0):
    # Set cursor position
    GL['r'] = r
    GL['c'] = c
    # Set dimensions
    GL['R'] = R
    GL['C'] = C
    # Build the map.
    GL['map'] = [ [' '] * GL['C'] for x in range(GL['R']) ]
def moveModelCursor(dr,dc):
    newR = GL['r'] + dr
    newC = GL['c'] + dc
    if newR >= 0 and newR < GL['R'] and newC >= 0 and newC < GL['C']:
        GL['r'] = newR
        GL['c'] = newC
def toggleModel(r,c):
    if GL['map'][r][c] == ' ':
        GL['map'][r][c] = '*'
    elif GL['map'][r][c] == '*':
        GL['map'][r][c] = ' '
    else:
        GL['map'][r][c] = '?'
def toggleModelAtCursor():
    toggleModel(GL['r'],GL['c'])
    
# support methods for tickModel()
def neighborModelCell(r,c,dr,dc):
    R = (r+dr)%GL['R']
    C = (c+dc)%GL['C']
    return (R,C)
def liveModelNeighborCount(r,c):
    ret = 0
    dx = (-1,0,1)
    from itertools import product
    f = lambda r,c,dr,dc : neighborModelCell(r,c,dr,dc)
    dx2 = [ f(r,c,ri,ci) for (ri,ci) in product(dx,dx) if (ri,ci) != (0,0) ]
    return len([ (ri,ci) for (ri,ci) in dx2 if GL['map'][ri][ci] == '*' ])
# Tick model, per Conway's Game of Life.
def tickModel():
    newMap = [ [' '] * GL['C'] for x in range(GL['R']) ]
    for r in range(GL['R']):
        for c in range(GL['C']):
            count = liveModelNeighborCount(r,c)
            if count < 2 or count > 3:
                newMap[r][c] = ' '
            elif count == 3:
                newMap[r][c] = '*'
            elif count == 2:
                newMap[r][c] = GL['map'][r][c]
    GL['map'] = newMap
# Immutable live neighbor count 
def liveImmutableModelNeighborCount(map,r,c):
    R = len(map)
    C = len(map[0])
    ret = 0
    dx = (-1,0,1)
    from itertools import product
    def f (r,c,dr,dc):
        RR = (r+dr)%R
        CC = (c+dc)%C
        return (RR,CC)
    dx2 = [ f(4,c,ri,ci) for (ri,ci) in product(dx,dx) if (ri,ci) != (0,0) ]
    return len([ (ri,ci) for (ri,ci) in dx2 if map[ri][ci] == '*'])
# Immutable tick
def tickImmutableModel(map):
    R = len(map)
    C = len(map[0])
    newMap = [ [' '] * C for x in range(R) ]
    for r in range(R):
        for c in range(C):
            count = liveImmutableModelNeighborCount(map,r,c)
            if count < 2 or count > 3:
                newMap[r][c] = ' '
            elif count == 3:
                newMap[r][c] = '*'
            elif count == 2:
                newMap[r][c] = map[r][c]
    newMap = tuple([ tuple(row) for row in newMap])
    return newMap
    

# View (all ncurses logic remains here)
def initView():
    GL['scr'] = curses.initscr()
    curses.noecho()
    curses.raw()
    GL['scr'].keypad(1)
    
def endView():
    curses.endwin()
    
def getKey():
    return GL['scr'].getch()
    
def drawView():
    GL['scr'].erase()
    R, C = GL['scr'].getmaxyx()
    lowR = (R - GL['R'])/2
    lowC = (C - GL['C'])/2
    
    # Draw the borders
    for r in range(GL['R']):
        GL['scr'].addch(r+lowR,lowC-1,'|')
        GL['scr'].addch(r+lowR,lowC+GL['C'],'|')
    for c in range(GL['C']):
        GL['scr'].addch(lowR-1,lowC+c,'-')
        GL['scr'].addch(lowR+GL['R'],lowC+c,'-')
    
    # Draw the map
    for r in range(GL['R']):
        for c in range(GL['C']):
            GL['scr'].addch(lowR+r,lowC+c,GL['map'][r][c])
    
    # Move the cursor to position as indicated by the model.
    GL['scr'].move(GL['r']+lowR, GL['c']+lowC)
    
    # Finally make sure it is drawn to the screen
    GL['scr'].refresh()
    
# Glue code (Controller?)
def main():
    from sys import argv
    if len(argv) < 3:
        print("Usage: %s [Rows] [Columns]" % argv[0])
        return None
    else:
        initModel(int(argv[1]),int(argv[2]))
        
    try:
        initView()
        GL['running'] = True
        while GL['running']:
            drawView()
            
            # Handle input
            key = getKey()
            # -- exit --
            if key == ord('q') or key == 3:
                GL['running'] = False
            # -- movement --
            elif key == ord('a'):
                moveModelCursor(0,-1)
            elif key == ord('d'):
                moveModelCursor(0, 1)
            elif key == ord('w'):
                moveModelCursor(-1,0)
            elif key == ord('s'):
                moveModelCursor( 1,0)
            # -- toggle cell --
            elif key == ord(' '):
                toggleModelAtCursor()
            # -- tick model --
            elif key == ord('t'):
                tickModel()
            # -- reset model --
            elif key == ord('r'):
                initModel(GL['R'],GL['C'], GL['r'], GL['c'])
            
        endView()
        print("Exited properly.")
    except:
        endView()
        print("Something went wrong.")
    
if __name__ == '__main__':
    main()