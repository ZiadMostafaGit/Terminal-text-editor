import argparse
import curses
import sys
import Buffer
import Window
import Cursor
import NormalMode
import SuperMode

# def is_it_ctrl(k):
#     if k==curses.KEY_CODE_YES:
#         return True


# def ctrl_NormalMode(k,cursor,buffer,window,args):
#     if k==19:
       


def is_ctrl_key(k):
    return k >= 1 and k <= 26

def is_ctrl_shift_key(k):
    return k >= 27 and k <= 30

def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as f:
        buffer = Buffer.Buffer(f.read().splitlines())

    window =Window.Window(curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor.Cursor()

   
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
        if k==9:
            k=stdscr.getch()
            SuperMode.Action(k,cursor,buffer,window,args)
        else:

            NormalMode.Action(k,cursor,buffer,window,args)
       

if __name__ == "__main__":
    curses.wrapper(main)




    
