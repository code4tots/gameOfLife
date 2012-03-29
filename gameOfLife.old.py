#!/usr/bin/python
# 3.27.2012
# gameOfLife.py

import curses
# Model stuff

# Global variables (saved in GL)
GL = {}
GL['running'] = False
GL['r'] = 0
GL['c'] = 0
GL['R'] = 10
GL['C'] = 30
GL['map'] = [ [0] * GL['C'] ] * GL['R']
def moveModelCursor(dr,dc):
    newR = GL['r'] + dr
    newC = GL['c'] + dc
    if newR >= 0 and newR < GL['R'] and newC >= 0 and newC < GL['C']:
        GL['r'] = newR
        GL['c'] = newC
    else:
        pass
def resetModel(R,C):
    GL['R'] = R
    GL['C'] = C
    GL['map'] = [ [0] * GL['C'] ] * GL['R']
def toggleModel(r,c):
    if GL['map'][r][c] == 0:
        GL['map'][r][c] = 1
    else:
        GL['map'][r][c] = 0
    
# Enter UI loop -- all ncurses logic remains here
def run():
    # Initialization
    stdscr = curses.initscr()
    curses.noecho()
    curses.raw()
    stdscr.keypad(1)
    # curses.curs_set(0)
    curses.mousemask(1)
    
    curses.endwin()
    
    # Some calculations.
    maxR, maxC = stdscr.getmaxyx()
    lowR = (maxR - GL['R'])/2
    lowC = (maxC - GL['C'])/2
    
    GL['running'] = True
    while GL['running']:
        # Draw model.
        # Clear
        stdscr.erase()
        # Draw border.
        for r in range(GL['R']):
            stdscr.addch(r+lowR,lowC-1,'|')
            stdscr.addch(r+lowR,lowC+GL['C'],'|')
        for c in range(GL['C']):
            stdscr.addch(lowR-1,c+lowC,'-')
            stdscr.addch(lowR+GL['R'],c+lowC,'-')
        # Draw map.
        for r in range(GL['R']):
            for c in range(GL['C']):
                toDraw = GL['map'][r][c]
                if toDraw == 0:
                    stdscr.addch(r+lowR,c+lowC,' ')
                elif toDraw == 1:
                    stdscr.addch(r+lowR,c+lowC,'*')
        # Move cursor to right position
        stdscr.move(GL['r']+lowR,GL['c']+lowC)
        stdscr.refresh()
        
        # Handle input.
        key = stdscr.getch()
        # -- exit -- (key == 3 ==> Ctrl-c)
        if key == ord('q') or key == 3: 
            GL['running'] = False
        elif key == curses.KEY_MOUSE:
            pass
        # -- movement --
        elif key == ord('a'):
            moveModelCursor(0,-1)
        elif key == ord('d'):
            moveModelCursor(0, 1)
        elif key == ord('w'):
            moveModelCursor(-1,0)
        elif key == ord('s'):
            moveModelCursor( 1,0)
        # -- Toggle position --
        elif key == ord(' '):
            #toggleModel(GL['r'],GL['c'])
            GL['map'][GL['r']][GL['c']] = 1
    
    # Clean up
    curses.endwin()
    print("Exited properly.")
    
def main():
    try:
        run()
    except:
        curses.endwin()
        print("Something was wrong.")
    
if __name__ == '__main__':
    main()