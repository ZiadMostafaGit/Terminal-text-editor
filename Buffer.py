
class Buffer:
    def __init__(self, lines):
        self.lines = lines
        self.copy_lines = []

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
    
        for row_index in range(start_row, end_row + 1):
            line = self.buffer[row_index]
            copied_part = line[start_col:end_col]
            self.copy_lines.append(copied_part)
            

        return self.copy_lines

# To paste the copied text at a specific cursor position
    def paste(self, cursor, copied_lines):
        if copied_lines is not None:
            row, col = cursor.row, cursor.col
            self.lines = self.lines[:row] + copied_lines + self.lines[row:]
            cursor.row += len(copied_lines)
            cursor.col = len(copied_lines[-1])