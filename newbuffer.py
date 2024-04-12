class Buffer:
    def __init__(self, lines):
        self.lines = lines
        self.copied_text = []

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

    def insert(self, cursor, character):
        row, col = cursor.row, cursor.col
        current_line = self.lines[row]
        new_line = current_line[:col] + character + current_line[col:]
        self.lines[row] = new_line
        cursor.move_right()

    def split(self, cursor):
        row, col = cursor.row, cursor.col
        current_line = self.lines[row]
        self.lines[row] = current_line[:col]
        self.lines.insert(row + 1, current_line[col:])

    def delete(self, cursor):
        row, col = cursor.row, cursor.col
        if col < len(self.lines[row]):
            current_line = self.lines[row]
            new_line = current_line[:col] + current_line[col + 1:]
            self.lines[row] = new_line
        elif row < len(self) - 1:
            self.lines[row] += self.lines.pop(row + 1)

    def copy(self, cursor):
        start_row, start_col = cursor.start_row, cursor.start_col
        end_row, end_col = cursor.end_row, cursor.end_col
        self.copied_text = []
        for row_index in range(start_row, end_row + 1):
            line = self.lines[row_index]
            copied_part = line[start_col:end_col]
            self.copied_text.append(copied_part)

    def paste(self, cursor):
        if self.copied_text:
            row, col = cursor.row, cursor.col
            self.lines = self.lines[:row] + self.copied_text + self.lines[row:]
            cursor.row += len(self.copied_text)
            cursor.col = len(self.copied_text[-1])
