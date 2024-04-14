
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
            
            


# To paste the copied text at a specific cursor position
    def paste(self, cursor):
        if len(self.copied_text) != 0:
            row, col = cursor.row, cursor.col
            self.lines = self.lines[:row] + self.copied_text + self.lines[row:]
            cursor.row += len(self.copied_text)
            cursor.col = len(self.copied_text[-1])
            
            
            
            
            




            
            
            
            