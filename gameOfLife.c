#include<stdlib.h>
#include<ncurses.h>
// model.
int running = FALSE;
char** map = NULL;
size_t Row = 0;
size_t Col = 0;
void deleteModelFromCharPtrPtr(char** map);
void deleteModel();
void initModel(size_t r, size_t c);
void randomizeModel(int seed);
int countLiveNeighborsOfModelAt(char** map, int r, int c);
void tickModel();
// Enter UI loop -- all ncurses logic remains here.
void run();
// main
int main(int argc, char* argv[]){
    initModel(10,10);
    randomizeModel(10);
    run();
    return 0;
}

// implementations.
// model.
void deleteModelFromCharPtrPtr(char** map){
    if (map != NULL){
        size_t r, c;
        for (r = 0; r < Row; r++){
            free(map[r]);
        }
        free(map);
    }
}
void deleteModel(){ deleteModelFromCharPtrPtr(map); }
void initModel(size_t r, size_t c){
    int ri, ci;
    
    deleteModel();
    Row = r;
    Col = c;
    
    map = malloc(Row*sizeof(char*));
    for (ri = 0; ri < Row; ri++){
        map[ri] = malloc(Col*sizeof(char));
        for (ci = 0; ci < Col; ci++){
            map[ri][ci] = 0;
        }
    }
}
void randomizeModel(int seed){
    int r, c;
    
    
    srand(seed);
    
    for (r = 0; r < Row; r++){
        for (c = 0; c < Col; c++){
            map[r][c] = rand() % 2;
        }
    }
}
int countLiveNeighborsOfModelAt(char** map, int r, int c){
    int dr, dc;
    int rr, cc;
    
    int ret = 0;
    for (dr = -1; dr <= 1; dr++){
        rr = (r + Row + dr) % Row;
        for (dc = -1; dc <= 1; dc++){
            if ( (dr == dc) && (dc == 0) ) continue;
            
            cc = (c + Col + dc) % Col;
            
            if (map[rr][cc] == 1){
                ret++;
            }
        }
    }
    return ret;
}
void tickModel(){
    int ri, ci;
    
    // create a copy
    char** cpy;
    cpy = malloc(Row*sizeof(char*));
    for (ri = 0; ri < Row; ri++){
        cpy[ri] = malloc(Col*sizeof(char));
        for (ci = 0; ci < Col; ci++){
            cpy[ri][ci] = map[ri][ci];
        }
    }
    
    // Now update the original
    for (ri = 0; ri < Row; ri++){
        for (ci = 0; ci < Col; ci++){
            switch (countLiveNeighborsOfModelAt(cpy,ri,ci)){
                case 2:
                    map[ri][ci] = cpy[ri][ci];
                    break;
                case 3:
                    map[ri][ci] = 1;
                    break;
                default: // less than 2 or more than 3
                    map[ri][ci] = 0;
                    break;
            }
        }
    }
    
    // Now free memory allocated for the copy
    deleteModelFromCharPtrPtr(cpy);
}

// Enter UI loop -- all ncurses logic remains here.
void run(){
    int maxR, maxC;
    int lowR, lowC;
    int r, c;
    char toDraw;
    
    initscr();
    raw();
    noecho();
    keypad(stdscr,TRUE);
    curs_set(0);
    
    running = TRUE;
    while (running){
        // draw.
        erase(); // clear
        
        // calculate borders
        getmaxyx(stdscr,maxR, maxC);
        // leave space for border.
        lowR = (maxR - Row) / 2;
        lowC = (maxC - Col) / 2;
        
        // draw border
        for (r = 0; r < Row; r++){
            mvaddch(lowR+r,lowC-1,'|');
            mvaddch(lowR+r,lowC+Col,'|');
        }
        for (c = 0; c < Col; c++){
            mvaddch(lowR-1,lowC+c,'-');
            mvaddch(lowR+Row,lowC+c,'-');
        }
        mvaddch(lowR-1,lowC+Col,'&');
        mvaddch(lowR-1,lowC-1,'&');
        mvaddch(lowR+Row,lowC+Col,'&');
        mvaddch(lowR+Row,lowC-1,'&');
        
        
        // draw map
        for (r = 0; r < Row; r++){
            for (c = 0; c < Col; c++){
                switch (map[r][c]) {
                    case 0:
                        toDraw = ' ';
                        break;
                    case 1:
                        toDraw = '*';
                        break;
                    default:
                        toDraw = '?';
                        break;
                }
                mvaddch(r+lowR,c+lowC,toDraw);
            }
        }
        refresh();
        
        // handle input.
        switch (getch()){
            case 3: // ctrl-c
                running = FALSE;
                break;
            case ' ':
                tickModel();
                break;
        }
    }
    
    endwin();
}
