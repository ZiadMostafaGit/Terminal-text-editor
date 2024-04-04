import argparse
import curses
import sys
import Window
import Cursor

class Buffer:
    def __init__(self, lines):
        self.lines = lines

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
