import curses
import argparse
import sys

class curser:
    


    def __init__(self, row=0, col=0 ):
        self.row = row
        self.col = col

    def move_up(self):
        if self.row > 0:
            self.row -= 1

    def move_down(self, buffer):

        if self.row < len(buffer) - 1:
            self.row += 1
        else:
            self.col=0
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
            self.move_down(buffer)    

    
    def move_tap_right(self, buffer):
        if self.col < len(buffer[self.row]):
            self.col += 5      

   
    def move_tap_left(self):
        if self.col>0:
            self.col-=5            


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
            cur.move_down(buffer)
        elif k==552:# the ctrl+left ascii
            cur.move_tap_left()
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
    cur = curser(0, 0)

    while True:
        stdscr.erase()

        # Adjust cursor position if it exceeds window boundaries
        if cur.row >= win.n_row:
            cur.row = win.n_row - 1
        if cur.col >= win.n_col:
            cur.col = win.n_col - 1

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



# def main(stdscr):
#     parser = argparse.ArgumentParser()
#     parser.add_argument("filename")
#     args = parser.parse_args()

#     with open(args.filename) as f:
#         buffer = f.readlines()

#     curses.curs_set(1)
#     win=window(curses.LINES - 1, curses.COLS - 1)
#     cur=curser(0,0)
#     while True:
#         stdscr.erase()
#         for row, line in enumerate(buffer[:win.n_row]):
#             stdscr.addstr(row, 0, line[:win.n_col])
#             stdscr.move(cur.row,cur.col)    

#         k = stdscr.getch()
#         Moving_Mode(k,cur,buffer)

#         stdscr.move(cur.row,cur.col)        
#         stdscr.refresh()

# if __name__ == "__main__":
#     curses.wrapper(main)






   