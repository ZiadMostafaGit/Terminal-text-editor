import curses
import NormalMode




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
    return k in [336,337,393,402]


# 336 is down 337 is up  393 is left and 402 is right








def highlight(k,cursor,buffer,window,args,stdscr):
    cursor.start_highlight()
    while is_shift_arrows(k):
        if k==336:
            k=curses.KEY_DOWN
        elif k==337:
                k=curses.KEY_UP
        elif k==393:
                k=curses.KEY_LEFT
        else:
            k=curses.KEY_RIGHT

        NormalMode.Action(k,cursor,buffer,window,args)
        loop(stdscr,buffer,window,cursor)
        k=stdscr.getch()

    cursor.end_highlight() 

