import argparse
import curses
import sys
import Buffer
import Window



class Cursor:
    def __init__(self, row=0, col=0,col_hint=None):
        self.row = row
        self.col = col
        self.col_hint=col if col_hint is None else col_hint

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, col):
        self._col = col
        self._col_hint = col

    # ...

    def _clamp_col(self, buffer):
        self._col = max(self._col_hint, len(buffer[self.row]))



    def up(self, buffer):
        if self.row > 0:
            self.row -= 1
            self._clamp_col(buffer)

    def down(self, buffer):
        if self.row < len(buffer) - 1:
            self.row += 1
            self._clamp_col(buffer)


    def _clamp_col(self, buffer):
        self.col = min(self.col, len(buffer[self.row]))

    def left(self, buffer):
        if self.col > 0:
            self.col -= 1
        elif self.row > 0:
            self.row -= 1
            self.col = len(buffer[self.row])
    
    
    def tap_left(self,buffer):
        if self.col-4 > 0:
            self.col -= 5
        elif self.row > 0:
            self.row -= 1
            self.col = len(buffer[self.row])
    


    def right(self, buffer,win):
        if self.col < len(buffer[self.row])and self._col<win.n_cols:
            self.col += 1
        elif self.row < len(buffer) - 1:
            self.row += 1
            self.col = 0



    def tap_right(self,buffer,win):
         if self.col+4 < len(buffer[self.row])and self._col<win.n_cols:
            self.col += 5
         elif self.row < len(buffer) - 1:
           self.row += 1
           self.col = 0

