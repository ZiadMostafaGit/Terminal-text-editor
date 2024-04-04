import argparse
import curses
import sys
import Buffer
import Window
import Cursor
import Action




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
        Action.Action(k,cursor,buffer,window,args)
       

if __name__ == "__main__":
    curses.wrapper(main)




    
