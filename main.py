import curses
import database

MENU = ['Start', 'Import Data', 'Exit']


def print_menu(stdscr, selected_row_idx):
    h, w = stdscr.getmaxyx()

    stdscr.clear()
    for idx, row in enumerate(MENU):
        x = w//2 - len(row)//2
        y = h//2 - len(MENU)//2 + idx
        if idx == selected_row_idx:
            stdscr.addstr(y, x, row, curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()


def main(stdscr):
    curses.curs_set(False)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row_idx = 0

    print_menu(stdscr, current_row_idx)

    while 1:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(MENU)-1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()
            stdscr.refresh()
            stdscr.getch()

            if MENU[current_row_idx] == 'Exit':
                exit(0)
            elif MENU[current_row_idx] == 'Start':
                pass
            elif MENU[current_row_idx] == 'Import Data':
                pass

        print_menu(stdscr, current_row_idx)
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
