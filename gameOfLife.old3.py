#!/usr/bin/python
# 3.28.2012
# 
# gameOfLife.py
#
# Another attempt at making the code more extensible/manageable.
# 
# ...
# curses inexplicably doesn't work.
# So I'm going to abandon this, and perhaps come back
# If I solve it.
# ...

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
        
    # move the cursor
    def moveCursor(self,dr,dc):
        if withinBounds(self.r+dr,self.c+dc):
            self.r , self.c = self.movePosition(self,self.r,self.c,dr,dc)
    
    # Const methods --> methods that doesn't change the instance.
    # Check whether given positions are within bounds
    def withinBounds(self,r,c):
        return (r >= 0 and r < self.R and c >= 0 and c < self.C)
    # Helper movement method
    def movePosition(self,r,c,dr,dc):
        return (r+dr)%self.R , (c+dc)%self.C
    


# PART 2 ::: View (all ncurses related logic)
class View:
    import curses
    
    def __init__(self):
            self.scr = None
        
    def initialize(self):
        print("enter initialized.")
        self.scr = View.curses.initscr()
        print("after View.curses.initscr().")
        
    def end(self):
        View.curses.endwin()
        
    def getKey(self):
        self.scr.endwin()

# PART 3 :: Controller (execution)
def main():
    view = View()
    try:
        view.initialize()
        print("initialized.")
        keepRunning = True
        while keepRunning:
            view.draw()
            key = view.getKey()
            if key == ord('q') or key == 3:
                keepRunning = False
                
        view.end()
        print("Exited properly.")
    except:
        view.end()
        print("Something went wrong.")
    
if __name__ == '__main__':
    main()
    import curses
    try:
        scr = curses.initscr()
    except:
        curses.endwin()
    