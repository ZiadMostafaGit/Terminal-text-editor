import curses
import curses.ascii
import sys




saved=False


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




def Super_action(k,cursor,buffer,window,args,stdscr):
     

    if k == 113:
        if saved: 
            sys.exit(0)


        else:
            #  Super_action(115,cursor,buffer,window,args,stdscr)
             sys.exit(0)    



    elif k==115:
        with open(args.filename, "w") as f:
            f.write("\n".join(buffer.lines))



    elif k==97:
      for i in range(2):
         filename = "mycopy.txt"
         with open(filename, "w") as file:
             
             
             
                size=len(buffer.copy_lines)
                if size<=0:
                    file.write(f"the copy_lines are empty")       
                else:
                    file.write(f"the copy has some thing and size is {size}\n")
                    for i in range(size):
                    
                        file.write(buffer.copy_lines[i]+"\n")
                
                
                # file.write(f"{cursor.start_row}\n")
                
                # file.write(f"{cursor.end_row}\n")
                
                # file.write(f"{cursor.start_col}\n")
                   
                # file.write(f"{cursor.end_col}\n")














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
    

     elif k == 10:#enter key to split
         buffer.split(cursor)
         cursor.row += 1
         cursor.col = 0
         

     elif k == 263:#backspace key to delete
         cursor.left(buffer)
         buffer.delete(cursor)
     


     elif k==552:#ctrl+left arrow
         
         cursor.tap_left(buffer)
         


     elif k==567:#ctrl+right arrow
         cursor.tap_right(buffer,window)





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

            Action(k,cursor,buffer,window,args,stdscr)
            loop(stdscr,buffer,window,cursor)
            k=stdscr.getch()

        cursor.end_highlight()
     
     
     
     elif k==24:#ctrl+x
            buffer.copy(cursor)
            
            
            
     elif k==22:
         buffer.paste(cursor)
               
     elif k==1:#ctrl+a
         
         cursor.highlight_all(buffer)
                         
                 
     else:
            buffer.insert(cursor, k,window)

