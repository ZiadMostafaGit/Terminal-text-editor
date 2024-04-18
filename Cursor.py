
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