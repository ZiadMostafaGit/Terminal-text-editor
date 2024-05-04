import argparse
import curses
import Buffer
import Window
import Cursor
import sys
import move
import os


 
 
def refresh(stdscr,buffer,window,cursor):
        stdscr.erase()
        for row, line in enumerate(buffer[window.row:window.row + window.n_rows]):
            if row == cursor.row - window.row and window.col > 0:
                line = "«" + line[window.col + 1:]
            if len(line) > window.n_cols:
                line = line[:window.n_cols - 1] + "»"
            stdscr.addstr(row, 0, line)
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
                    move.up(buffer, cursor, window)
                elif k == curses.KEY_DOWN:
                    move.down(buffer, cursor, window)
                elif k == curses.KEY_LEFT:
                    move.left(buffer, cursor, window)
                elif k == curses.KEY_RIGHT:
                    move.right(buffer, cursor, window)
                elif k == 554:  # ctrl+left arrow
                    cursor.tap_left(buffer)
                elif k == 569:  # ctrl+right arrow
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
            move.up(buffer,cursor,window)
        
        
        elif k==curses.KEY_DOWN:
            move.down(buffer,cursor,window)
        
        elif k==curses.KEY_LEFT:
            move.left(buffer,cursor,window)
        
        
        elif k==curses.KEY_RIGHT:
            move.right(buffer,cursor,window)
        
        elif k==554:#ctrl+left arrow
         
          cursor.tap_left(buffer)
        
        elif k==569:#ctrl+right arrow
           cursor.tap_right(buffer,window)

        
        
        
        #highlight
        elif k == ord('h'):
            cursor.start_highlight()
            while k != 27:
                if k == curses.KEY_UP:
                    move.up(buffer, cursor, window)
                elif k == curses.KEY_DOWN:
                    move.down(buffer, cursor, window)
                elif k == curses.KEY_LEFT:
                    move.left(buffer, cursor, window)
                elif k == curses.KEY_RIGHT:
                    move.right(buffer, cursor, window)
                elif k == 554:  # ctrl+left arrow
                    cursor.tap_left(buffer)
                elif k == 569:  # ctrl+right arrow
                    cursor.tap_right(buffer, window)
                refresh(stdscr, buffer, window, cursor)
                k = stdscr.getch()

                if k == ord('c'):
                    cursor.end_highlight()
                    buffer.copy(cursor)
                    break  # Exit the refresh if 'c' is pressed
                
                if k==ord('x'):
                    cursor.end_highlight()
                    buffer.cut(cursor)
                    break
                if k==263:
                    cursor.end_highlight()
                    buffer.delete_highlighted(cursor)
                    break    

            if k != ord('c') and k!=ord('x')and k!=263:
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





class Window:

    def __init__(self, n_rows, n_cols, row=0, col=0):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.row = row
        self.col = col

    @property
    def bottom(self):
        return self.row + self.n_rows - 1

    def up(self, cursor):
        if cursor.row == self.row - 1 and self.row > 0:
            self.row -= 1

    def down(self, buffer, cursor):
        if cursor.row == self.bottom + 1 and self.bottom < len(buffer) - 1:
            self.row += 1


    def translate(self, cursor):
        return cursor.row - self.row, cursor.col - self.col
    

    def horizontal_scroll(self, cursor, left_margin=5, right_margin=2):
        n_pages = cursor.col // (self.n_cols - right_margin)
        self.col = max(n_pages * self.n_cols - right_margin - left_margin, 0)








def up(buffer,cursor,window):
    cursor.up(buffer)
    window.up(cursor)
    window.horizontal_scroll(cursor)
    
    

def down(buffer,cursor,window):
    cursor.down(buffer)
    window.down(buffer,cursor)
    window.horizontal_scroll(cursor)
    
    
def left(buffer,cursor,window):
    cursor.left(buffer)
    window.up(cursor)
    window.horizontal_scroll(cursor)
    
    
def right(buffer,cursor,window):
    cursor.right(buffer,window)
    window.down(cursor,window)
    window.horizontal_scroll(cursor)
    
        
    
    

class Cursor:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col
        self.col_hint=self.col
        self.start_row=0
        self.start_col=0
        self.end_row=0
        self.end_col=0
        self.max_col=0
        
        

    def up(self, buffer):
        if self.row > 0:
            if len(buffer[self.row-1])==0:
                
                self.col=0
            else:
                self.col=self.col_hint        
            self.row -= 1

    def down(self, buffer):
        if self.row < len(buffer) - 1:
            if len(buffer[self.row+1])==0:
                self.col=0
            else:
                self.col=self.col_hint    
            self.row += 1
    

    def left(self, buffer):
        if self.col > 0:
            self.col -= 1
        elif self.row > 0:
            self.row -= 1
            self.col = len(buffer[self.row])

        self.col_hint=self.col
    
    def tap_left(self,buffer):
        if self.col-4 > 0:
            self.col -= 5
        elif self.row > 0:
            self.row -= 1
            self.col = len(buffer[self.row])

        self.col_hint=self.col


    def right(self, buffer,win):
        if self.col < len(buffer[self.row])and self.col<win.n_cols:
            self.col += 1
        elif self.row < len(buffer) - 1:
            self.row += 1
            self.col = 0
        self.col_hint=self.col
    


    def tap_right(self,buffer,win):
         if self.col+4 < len(buffer[self.row])and self.col<win.n_cols:
            self.col += 5
         elif self.row < len(buffer) - 1:
           self.row += 1
           self.col = 0
         self.col_hint=self.col


    def start_highlight(self):
        
        self.start_row,self.start_col=self.row,self.col


    def end_highlight(self):
        self.end_row,self.end_col=self.row,self.col
    
    
    
    
    def highlight_all(self,buffer):
        self.start_row,self.start_col=0,0
        
        
        for i in buffer:
            if len(i)>self.max_col:
                self.max_col=len(i)     
        self.end_row,self.end_col=len(buffer)-1,self.max_col




class Buffer:
    def __init__(self, lines):
        self.lines = lines
        self.copied_text = []



    def __len__(self):
        return len(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

    def insert(self, cursor, string,win):
        row, col = cursor.row, cursor.col
        current = self.lines[row]
        new = current[:col] + chr(string) + current[col:]
        self.lines[row] = new
        cursor.right(self.lines,win)


    def split(self, cursor):
        row, col = cursor.row, cursor.col
        current = self.lines[row]
        self.lines[row] = current[:col]
        self.lines.insert(row + 1, current[col:])
        # cursor.down(self.lines)

    def delete(self, cursor):
        row, col = cursor.row, cursor.col
        if col < len(self[row]):
            current = self.lines[row]
            new = current[:col] + current[col + 1:]
            self.lines[row] = new
        elif row < len(self) - 1:
            self.lines[row] = self.lines[row] + self.lines.pop(row + 1)
    



    def delete_highlighted(self,cursor):
        start_row, end_row = cursor.start_row, cursor.end_row
        start_col, end_col = cursor.start_col, cursor.end_col
        
        self.lines=self.lines[:start_row]+self.lines[end_row:]
       






    
    def copy(self, cursor):
        start_row, end_row = cursor.start_row, cursor.end_row
        start_col, end_col = cursor.start_col, cursor.end_col
        self.copied_text.clear()
        
        for row_index in range(start_row, end_row+1):
            if row_index==end_row:
                if len(self.lines[row_index])>0:
                    line = self.lines[row_index]
                    copied_part = line[start_col:end_col]
                    self.copied_text.append(copied_part)
                
            else:
                if len(self.lines[row_index])>0:        
                    line = self.lines[row_index]
                    self.copied_text.append(line)
            
            


    def cut(self, cursor):
        start_row, end_row = cursor.start_row, cursor.end_row
        start_col, end_col = cursor.start_col, cursor.end_col
        self.copy(cursor)  # Call copy to store the text in clipboard

        if start_row == end_row:
            self.lines[start_row] = self.lines[start_row][:start_col] + self.lines[start_row][end_col:]
        else:
            self.lines[start_row] = self.lines[start_row][:start_col]
            self.lines[end_row] = self.lines[end_row][end_col:]

            if end_row > start_row + 1:
                del self.lines[start_row + 1:end_row]




# To paste the copied text at a specific cursor position
    def paste(self, cursor):
        if len(self.copied_text) != 0:
            row, col = cursor.row, cursor.col
            self.lines = self.lines[:row] + self.copied_text + self.lines[row:]
            cursor.row += len(self.copied_text)
            cursor.col = len(self.copied_text[-1])
            
            
            
            
            
    def rewine(self,cursor):
        pass



            
            
            
                                     