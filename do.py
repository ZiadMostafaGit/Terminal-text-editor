import argparse
import curses
import Buffer
import Window
import Cursor
import sys
import move
import os

line_number=1

def refresh(stdscr, buffer, window, cursor):
    stdscr.erase()
    

      # Initialize line number
    for row, line in enumerate(buffer[window.row:window.row + window.n_rows]):
        if row == cursor.row - window.row and window.col > 0:
            line = "«" + line[window.col + 1:]
        if len(line) > window.n_cols:
            line = line[:window.n_cols - 1] + "»"
        stdscr.addstr(row, 0, f"{line_number:3d} {line}")  # Display line number
        line_number += 1  # Increment line number
    stdscr.move(*window.translate(cursor))

def split (cursor,buffer):
    buffer.split(cursor)
    cursor.row += 1
    cursor.col = 0


def delete(cursor,buffer):
     cursor.left(buffer)
     buffer.delete(cursor)



def main(stdscr):
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    if os.path.exists(args.filename): 
        with open(args.filename) as f:
            buffer = Buffer.Buffer(f.read().splitlines())
    else:
        with open(args.filename, 'w+') as f:
            f.write(f" \n")
            f.seek(0)
            buffer = Buffer.Buffer(f.read().splitlines())

    window =Window.Window(curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor.Cursor()

   
    while True:
        
        refresh(stdscr,buffer,window,cursor)
        k = stdscr.getch()
        
        
        #insert        
        # insert        
        if k == ord('i'):
            while True:
                k = stdscr.getch()
                if k == 27:  # Esc char
                    break  # Exit insert mode loop
                elif k == 10:
                    split(cursor,buffer)
                elif k == curses.KEY_UP:
                    move.up(buffer, cursor, window,line_number)
                elif k == curses.KEY_DOWN:
                    move.down(buffer, cursor, window,line_number)
                elif k == curses.KEY_LEFT:
                    move.left(buffer, cursor, window)
                elif k == curses.KEY_RIGHT:
                    move.right(buffer, cursor, window)
                elif k == 560:  # ctrl+left arrow
                    cursor.tap_left(buffer)
                elif k == 575:  # ctrl+right arrow
                    cursor.tap_right(buffer, window)
                elif k == 263:
                    delete(cursor, buffer)
                else:
                    buffer.insert(cursor, k, window)
                refresh(stdscr, buffer, window, cursor)




        #save
        elif k==ord('s'):
              with open(args.filename, "w") as f:
                f.write("\n".join(buffer.lines))      
    
    
    
        #quit
        elif k==ord('q'):
            sys.exit(0)
        
        
        
        #moving
        elif k==curses.KEY_UP:
            move.up(buffer,cursor,window,line_number)
        
        
        elif k==curses.KEY_DOWN:
            move.down(buffer,cursor,window,line_number)
        
        elif k==curses.KEY_LEFT:
            move.left(buffer,cursor,window)
        
        
        elif k==curses.KEY_RIGHT:
            move.right(buffer,cursor,window)
        
        elif k==560:#ctrl+left arrow
         
          cursor.tap_left(buffer)
        
        elif k==575:#ctrl+right arrow
           cursor.tap_right(buffer,window)

        
        
        
        #highlight
        elif k == ord('h'):
            cursor.start_highlight()
            while k != 27:
                if k == curses.KEY_UP:
                    move.up(buffer, cursor, window,line_number)
                elif k == curses.KEY_DOWN:
                    move.down(buffer, cursor, window,line_number)
                elif k == curses.KEY_LEFT:
                    move.left(buffer, cursor, window)
                elif k == curses.KEY_RIGHT:
                    move.right(buffer, cursor, window)
                elif k == 560:  # ctrl+left arrow
                    cursor.tap_left(buffer)
                elif k == 575:  # ctrl+right arrow
                    cursor.tap_right(buffer, window)
                refresh(stdscr, buffer, window, cursor)
                k = stdscr.getch()

                if k == ord('c'):
                    cursor.end_highlight()
                    buffer.copy(cursor)
                    break  # Exit the refresh if 'c' is pressed
                
            if k != ord('c'):
                cursor.end_highlight()

        
        elif k==10:
            split(cursor,buffer)
            
            
        elif k== 263:
            delete(cursor,buffer)
        
     
        elif k==ord('c'):#ctrl+x
            buffer.copy(cursor)
        
        
        elif k==ord('v'):
            buffer.paste(cursor)
            
        elif k==97:
            cursor.highlight_all(buffer)            
        
        

if __name__ == "__main__":
   res= curses.wrapper(main)

 
 
 
# def refresh(stdscr,buffer,window,cursor):
#         stdscr.erase()
#         for row, line in enumerate(buffer[window.row:window.row + window.n_rows]):
#             if row == cursor.row - window.row and window.col > 0:
#                 line = "«" + line[window.col + 1:]
#             if len(line) > window.n_cols:
#                 line = line[:window.n_cols - 1] + "»"
#             stdscr.addstr(row, 0, line)
#         stdscr.move(*window.translate(cursor))
