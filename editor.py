import curses
import argparse
import sys





# ...

class Buffer:
    def __init__(self, lines):
        self.lines = lines

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, index):
        return self.lines[index]
    

    def insert(self,cur,k,buffer,win):
        row,col=cur.row,cur.col
        current=self.lines.pop(row)
        new=current[:col]+chr(k)+current[col:]
        self.lines.insert(row,new)
        if cur.col < win.n_col-1:
            cur.col += 1
        else :
            cur.col=0
            cur.move_down()
        

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


class window:

    def __init__(self, n_rows, n_cols, row=0, col=0):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.row = row
        self.col = col

    @property
    def bottom(self):
        return self.row + self.n_rows - 1

    def up(self, cursor):
        if cursor.row == self.row - 1 and self.row > 0:
            self.row -= 1

    def down(self, buffer, cursor):
        if cursor.row == self.bottom + 1 and self.bottom < len(buffer) - 1:
            self.row += 1




def Moving_Mode(k,cur,buffer,win):
        if k == 27:  
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

        else:
            buffer.insert(cur,k,buffer,win)



def printing(buffer,cur,win,stdscr):
    stdscr.erase()
    for row, line in enumerate(buffer[:win.n_row]):
            stdscr.addstr(row, 0, line[:win.n_col])

    stdscr.move(cur.row, cur.col)
    stdscr.refresh()







def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as f:
        buffer = Buffer(f.read().splitlines())

    curses.curs_set(1)
    win = window(curses.LINES - 1, curses.COLS - 1)
    cur = curser(0, 0,win)

    while True:
       
        printing(buffer,cur,win,stdscr)
        k = stdscr.getch()
        Moving_Mode(k, cur, buffer,win)
        stdscr.move(cur.row, cur.col)
        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)







   