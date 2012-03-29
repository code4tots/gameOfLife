#!/usr/bin/python
# 3.28.2012
#
# The last one had inexplicable failure with curses,
# So this time, I'll start with curses.

# PART 1 ::: Model
class Model:
    # Constructors
    def __init__(self,R,C,r=0,c=0):
        self.R, self.C = R, C
        self.r, self.c = r, c
        self.running = False
        self.map = [ [' '] * C for x in range(R) ]
    @staticmethod
    def fromDimensions(R,C):
        return Model(R,C)
    @staticmethod
    def fromMap(map):
        R , C = len(map) , len(map[0])
        
        ret = Model(R,C)
        ret.map = [ [ map[r][c] for c in range(C) ] for row in range(R) ]
        return ret
    @staticmethod
    def fromAnotherModel(model):
        ret = Model.fromMap(model.map)
        ret.r, ret.c = model.r, model.c
        return ret
        
    
    def reset(self):
        self.map = [ [' '] * self.C for x in range(self.R) ]
    
    # move the cursor
    def moveCursor(self,dr,dc):
        if self.withinBounds(self.r+dr,self.c+dc):
            self.r , self.c = self.movePosition(self.r,self.c,dr,dc)
    
    # toggle position
    def toggle(self):
        if self.map[self.r][self.c] == ' ':
            self.map[self.r][self.c] = '*'
        elif self.map[self.r][self.c] == '*':
            self.map[self.r][self.c] = ' '
        else:
            self.map[self.r][self.c] = '?'
            
    # tick per Conway's game of life
    def tick(self):
        newMap = [ [' '] * self.C for x in range(self.R) ]
        for r in range(self.R):
            for c in range(self.C):
                count = self.liveNeighborCount(r,c)
                if count < 2 or count > 3:
                    newMap[r][c] == ' '
                elif count == 3:
                    newMap[r][c] = '*'
                elif count == 2:
                    newMap[r][c] = self.map[r][c]
        self.map = newMap
            
    # Const methods --> methods that doesn't change the instance.
    # Check whether given positions are within bounds
    def withinBounds(self,r,c):
        return (r >= 0 and r < self.R and c >= 0 and c < self.C)
    # Helper movement method
    def movePosition(self,r,c,dr,dc):
        return (r+dr)%self.R , (c+dc)%self.C
    # Helper for tick
    def liveNeighborCount(self,r,c):
        ret = 0
        dx = (-1,0,1)
        from itertools import product
        f = lambda r,c,dr,dc : self.movePosition(r,c,dr,dc)
        dx2 = [ f(r,c,ri,ci) for (ri,ci) in product(dx,dx) if (ri,ci) != (0,0) ]
        return len([ (ri,ci) for (ri,ci) in dx2 if self.map[ri][ci] == '*' ])

# PART 2 ::: View (all ncurses related logic)
class View:
    import curses
    KEY_LEFT = curses.KEY_LEFT
    KEY_RIGHT = curses.KEY_RIGHT
    KEY_UP = curses.KEY_UP
    KEY_DOWN = curses.KEY_DOWN
    
    def __init__(self):
        self.scr = None
        self.R = 0
        self.C = 0
        self.lowR = 0
        self.lowC = 0
    
    # setup and cleanup code
    def cleaup(self):
        View.curses.endwin()
        
    def initialize(self):
        self.scr = View.curses.initscr()
        View.curses.noecho()
        View.curses.raw()
        self.scr.keypad(1)
    
    # input
    def getKey(self):
        return self.scr.getch()
        
    # draw code.
    def draw(self, map, r, c):
        # erase the screen
        self.scr.erase()
        
        # Calculations
        R = len(map)
        C = len(map[0])
        self.R = R
        self.C = C
        self.calculatelowRC()
        
        # Actual drawing
        self.drawBorder()
        self.drawMap(map)
        self.scr.move(self.lowR+r,self.lowC+c)
        
        # make sure it shows up on screen
        self.scr.refresh()
    # Helpers for draw. Should only be called by draw,
    # since they don't call erase() or refresh()
    def calculatelowRC(self):
        maxR, maxC = self.scr.getmaxyx()
        self.lowR = (maxR - self.R)/2
        self.lowC = (maxC - self.C)/2
    def drawBorder(self):
        for r in range(self.R):
            self.scr.addch(r+self.lowR,self.lowC-1,'|')
            self.scr.addch(r+self.lowR,self.lowC+self.C,'|')
        for c in range(self.C):
            self.scr.addch(self.lowR-1,self.lowC+c,'-')
            self.scr.addch(self.lowR+self.R,self.lowC+c,'-')
    def drawMap(self, map):
        for r in range(self.R):
            for c in range(self.C):
                self.scr.addch(self.lowR+r,self.lowC+c,map[r][c])

# PART 3 :: Controller (execution)
def main():
    from sys import argv
    if len(argv) < 3:
        print("Usage: %s [Rows] [Columns]" % argv[0])
    else:
    
        view = View()
        model = Model.fromDimensions(int(argv[1]),int(argv[2]))
        try:
            view.initialize()
        
            running = True
            while running:
                view.draw(model.map, model.r, model.c)
                key = view.getKey()
            
                # -- exit --
                if key == 3 or key == ord('q'):
                    running = False
                # -- movement --
                elif key == ord('a') or key == View.KEY_LEFT:
                    model.moveCursor(0,-1)
                elif key == ord('d') or key == View.KEY_RIGHT:
                    model.moveCursor(0, 1)
                elif key == ord('w') or key == View.KEY_UP:
                    model.moveCursor(-1,0)
                elif key == ord('s') or key == View.KEY_DOWN:
                    model.moveCursor( 1,0)
                # -- toggle char --
                elif key == ord(' '):
                    model.toggle()
                # -- tick --
                elif key == ord('t'):
                    model.tick()
                # -- reset --
                elif key == ord('r'):
                    model.reset()
        
        finally:
            view.cleaup()
        
if __name__ == '__main__':
    main()