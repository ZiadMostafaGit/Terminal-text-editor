import curses
import argparse
import sys

class curser:
    def __init__(self, row, col,win ):
        self.row = row
        self.col = col
        self.win=win

    def move_up(self):
        if self.row > 0:
            self.row -= 1
        else:
            self.row=self.win.n_row-1    

    def move_down(self):

        if self.row < self.win.n_row:
            self.row += 1
        else:
            self.row=0    

    def move_left(self,buffer):
        if self.col > 0:
            self.col -= 1
        else:
            self.col=len(buffer[self.row-1])
            self.move_up()    

    def move_right(self, buffer):
        if self.col < len(buffer[self.row]):
            self.col += 1
        else :
            self.col=0
            self.move_down()    

    
    def move_tap_right(self, buffer):
        if self.col < len(buffer[self.row]):
            self.col += 5
        else:
            self.col=0
            self.move_down()           

   
    def move_tap_left(self,buffer):
        if self.col>0:
            self.col-=5
        else:
            self.col=len(buffer[self.row-1])
            self.move_up()                


class  window:
    def __init__(self,n_row,n_col) -> None:
        self.n_row=n_row
        self.n_col=n_col




def Moving_Mode(k,cur,buffer):
        if k == ord('q'):  
            sys.exit(0)
        elif k == curses.KEY_LEFT: 
            cur.move_left(buffer)
        elif k == curses.KEY_RIGHT:
            cur.move_right(buffer)
        elif k == curses.KEY_UP:
            cur.move_up()
        elif k == curses.KEY_DOWN:
            cur.move_down()
        elif k==552:# the ctrl+left ascii
            cur.move_tap_left(buffer)
        elif k==567:#the ctrl +right ascii
            cur.move_tap_right(buffer)   







def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as f:
        buffer = f.readlines()

    curses.curs_set(1)
    win = window(curses.LINES - 1, curses.COLS - 1)
    cur = curser(0, 0,win)

    while True:
        stdscr.erase()


        for row, line in enumerate(buffer[:win.n_row]):
            stdscr.addstr(row, 0, line[:win.n_col])

       

        stdscr.move(cur.row, cur.col)
        stdscr.refresh()

        k = stdscr.getch()
        Moving_Mode(k, cur, buffer)

        stdscr.move(cur.row, cur.col)
        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)







   