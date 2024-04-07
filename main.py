import argparse
import curses
import sys
import Buffer
import Window
import Cursor
import NormalMode
import SuperMode
import Newcursor
# import cursor3
       
# hello iam ziad mostafa and 
# this is my first
#  software
# ever 



def is_tab_key(k):
    return  k==9


def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as f:
        buffer = Buffer.Buffer(f.read().splitlines())

    window =Window.Window(curses.LINES - 1, curses.COLS - 1)
    cursor = Newcursor.Cursor()

   
    while True:
        stdscr.erase()
        for row, line in enumerate(buffer[window.row:window.row + window.n_rows]):
            if row == cursor.row - window.row and window.col > 0:
                line = "«" + line[window.col + 1:]
            if len(line) > window.n_cols:
                line = line[:window.n_cols - 1] + "»"
            stdscr.addstr(row, 0, line)
        stdscr.move(*window.translate(cursor))
        k = stdscr.getch()
        if is_tab_key(k):       
            k=stdscr.getch()
            SuperMode.Action(k,cursor,buffer,window,args)
        else:

            NormalMode.Action(k,cursor,buffer,window,args)
       

if __name__ == "__main__":
    curses.wrapper(main)




    