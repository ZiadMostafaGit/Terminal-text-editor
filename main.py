import argparse
import curses
import Buffer
import Window
import Cursor
import action


   




def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as f:
        buffer = Buffer.Buffer(f.read().splitlines())

    window =Window.Window(curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor.Cursor()

   
    while True:
        
        action.loop(stdscr,buffer,window,cursor)
        k = stdscr.getch()
        if k==27:
            k=stdscr.getch()
            action.Super_action(k,cursor,buffer,window,args,stdscr)
                        
        action.Action(k,cursor,buffer,window,args,stdscr)

       
       

if __name__ == "__main__":
   res= curses.wrapper(main)

 