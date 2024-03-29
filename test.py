import argparse
import curses
import sys

class Buffer:
    def _init_(self, lines):
        self.lines = lines

    def _len_(self):
        return len(self.lines)

    def _getitem_(self, index):
        return self.lines[index]

    def insert(self, cursor, string):
        row, col = cursor.row, cursor.col
        current = self.lines[row]
        new = current[:col] + string + current[col:]
        self.lines[row] = new

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

class Cursor:
    def _init_(self, row=0, col=0):
        self.row = row
        self.col = col

    def up(self, buffer):
        if self.row > 0:
            self.row -= 1
            self.col = min(self.col, len(buffer[self.row]))

    def down(self, buffer):
        if self.row < len(buffer) - 1:
            self.row += 1
            self.col = min(self.col, len(buffer[self.row]))

    def left(self, buffer):
        if self.col > 0:
            self.col -= 1
        elif self.row > 0:
            self.row -= 1
            self.col = len(buffer[self.row])

    def right(self, buffer):
        if self.col < len(buffer[self.row]):
            self.col += 1
        elif self.row < len(buffer) - 1:
            self.row += 1
            self.col = 0

class Window:
    def _init_(self, n_rows, n_cols, row=0, col=0):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.row = row
        self.col = col

    @property
    def bottom(self):
        return self.row + self.n_rows - 1

    def up(self, cursor, buffer):
        if cursor.row == self.row and self.row > 0:
            self.row -= 1
            self.horizontal_scroll(cursor, buffer)

    def down(self, cursor, buffer):
        if cursor.row == self.bottom and self.bottom < len(buffer) - 1:
            self.row += 1
            self.horizontal_scroll(cursor, buffer)

    def horizontal_scroll(self, cursor, buffer, left_margin=5, right_margin=2):
        n_pages = cursor.col // (self.n_cols - right_margin)
        self.col = max(n_pages * self.n_cols - right_margin - left_margin, 0)
        self.col = min(self.col, len(buffer[cursor.row]) - self.n_cols + right_margin)

    def translate(self, cursor):
        return cursor.row - self.row, cursor.col - self.col

def main(stdscr):
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename) as f:
        buffer = Buffer(f.read().splitlines())

    window = Window(curses.LINES - 1, curses.COLS - 1)
    cursor = Cursor()

    while True:
        stdscr.erase()
        for row, line in enumerate(buffer[window.row:window.row + window.n_rows]):
            if row == cursor.row - window.row and window.col > 0:
                line = "«" + line[window.col + 1:]
            if len(line) > window.n_cols:
                line = line[:window.n_cols - 1] + "»"
            stdscr.addstr(row, 0, line)
        stdscr.move(*window.translate(cursor))

        k = stdscr.getkey()
        if k == "q":
            sys.exit(0)
        elif k == "KEY_UP":
            cursor.up(buffer)
            window.up(cursor, buffer)
        elif k == "KEY_DOWN":
            cursor.down(buffer)
            window.down(cursor, buffer)
        elif k == "KEY_LEFT":
            cursor.left(buffer)
            window.horizontal_scroll(cursor, buffer)
        elif k == "KEY_RIGHT":
            cursor.right(buffer)
            window.horizontal_scroll(cursor, buffer)
        elif k == "\n":
            buffer.split(cursor)
            cursor.row += 1
            cursor.col = 0
        elif k == "\x7f":
            cursor.left(buffer)
            buffer.delete(cursor)
        else:
            buffer.insert(cursor, k)

if __name__ == "_main_":
    curses.wrapper(main)
