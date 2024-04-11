import curses
import curses.ascii
import sys




def is_tab_key(k):
    return  k==9



def loop(stdscr,buffer,window,cursor):
        stdscr.erase()
        for row, line in enumerate(buffer[window.row:window.row + window.n_rows]):
            if row == cursor.row - window.row and window.col > 0:
                line = "«" + line[window.col + 1:]
            if len(line) > window.n_cols:
                line = line[:window.n_cols - 1] + "»"
            stdscr.addstr(row, 0, line)
        stdscr.move(*window.translate(cursor))



def is_shift_arrows(k):
    return k in [336,337,393,402,83,67,86]


def Action(k,cursor,buffer,window,args,stdscr):

     if k == curses.KEY_UP:
         cursor.up(buffer)
         window.up(cursor)
         window.horizontal_scroll(cursor)
     elif k == curses.KEY_DOWN:
         cursor.down(buffer)
         window.down(buffer, cursor)
         window.horizontal_scroll(cursor)
     elif k == curses.KEY_LEFT: 
         cursor.left(buffer)
         window.up(cursor)
         window.horizontal_scroll(cursor)
     elif k == curses.KEY_RIGHT:
         cursor.right(buffer,window)
         window.down(buffer, cursor)
         window.horizontal_scroll(cursor)
    
     elif k == 10:
         buffer.split(cursor)
         cursor.row += 1
         cursor.col = 0
     elif k == 263:
         cursor.left(buffer)
         buffer.delete(cursor)
     elif k==554:
         cursor.tap_left(buffer)
         
     elif k==569:
         cursor.tap_right(buffer,window)

     elif k == 113:
            sys.exit(0)


     elif k==115:
        with open(args.filename, "w") as f:
            f.write("\n".join(buffer.lines))



     elif  is_shift_arrows(k):
        cursor.start_highlight()
        while is_shift_arrows(k):
            if k==336:
                k=curses.KEY_DOWN
            elif k==337:
                    k=curses.KEY_UP
            elif k==393:
                    k=curses.KEY_LEFT
            elif k==402:
                k=curses.KEY_RIGHT
            elif k==67:
                 buffer.copy(cursor)

            Action(k,cursor,buffer,window,args)
            loop(stdscr,buffer,window,cursor)
            k=stdscr.getch()

        cursor.end_highlight()          
                 
     else:
            buffer.insert(cursor, k,window)

