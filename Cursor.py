import argparse
import curses
import sys
import Buffer
import Window



class Cursor:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col
        self.col_hint=self.col

         
        

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
