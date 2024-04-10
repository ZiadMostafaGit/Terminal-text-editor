import curses
import curses.ascii
import sys
def Action(k,cursor,buffer,window,args):

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
     elif k==552:
         cursor.tap_left(buffer)
         
     elif k==567:
         cursor.tap_right(buffer,window)
                 
     else:
            buffer.insert(cursor, k,window)

