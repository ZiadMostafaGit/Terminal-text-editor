import argparse
import curses
import Buffer
import Window
import Cursor
import NormalMode
import SuperMode
import highlight
import help_func 









def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as f:
        buffer = Buffer.Buffer(f.read().splitlines())

    window =Window.Window(curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor.Cursor()

   
    while True:
        
        highlight.loop(stdscr,buffer,window,cursor)
        k = stdscr.getch()

        if help_func.is_tab_key(k):       
            k=stdscr.getch()
            
            SuperMode.Action(k,cursor,buffer,window,args,stdscr)


        elif help_func.is_shift_arrows(k):
            highlight.highlight(k,cursor,buffer,window,args,stdscr)    
               

        else:

            NormalMode.Action(k,cursor,buffer,window,args)

       
       

if __name__ == "__main__":
   res= curses.wrapper(main)

 