import curses

def main(stdscr):
    while True:
        key = stdscr.getch()
        stdscr.clear()
        stdscr.addstr(0, 0, "Key pressed: {}".format(key))
        stdscr.refresh()

        # Exit the program when 'q' is pressed
        if key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)
