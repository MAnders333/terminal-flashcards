import curses
import database
import pandas as pd
import random

MAIN_MENU = ['Start', 'Import Data', 'Exit']


ASCII_VIM_KEYS = {
    "h": 104,
    "j": 106,
    "k": 107,
    "l": 108
}


def print_menu(stdscr, menu, selected_row_idx):
    h, w = stdscr.getmaxyx()

    stdscr.clear()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.addstr(y, x, row, curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()


def get_language_menu(Database):
    language_menu = ['Create New Language']

    languages = Database.tables
    if len(languages) > 0:
        for language in languages:
            language_menu.append(language)

    language_menu.append('Exit')

    return language_menu


def get_user_input(stdscr):
    user_input = ''
    while 1:
        key = stdscr.getkey()
        if key != '\n':
            user_input = user_input + key
            stdscr.clear()
            curses.curs_set(1)
            stdscr.addstr(user_input)
            stdscr.refresh()
        else:
            curses.curs_set(0)
            break
    return user_input


def get_language(stdscr, Database):
    language_menu = get_language_menu(Database)
    language_menu_idx = 0
    print_menu(stdscr, language_menu, language_menu_idx)

    while 1:
        key = stdscr.getch()
        if key in [curses.KEY_UP, ASCII_VIM_KEYS["k"]] and language_menu_idx > 0:
            language_menu_idx -= 1
        elif key in [curses.KEY_DOWN, ASCII_VIM_KEYS["j"]] and language_menu_idx < len(language_menu)-1:
            language_menu_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if language_menu[language_menu_idx] == 'Exit':
                break
            elif language_menu[language_menu_idx] == 'Create New Language':
                stdscr.clear()
                stdscr.addstr("Type in language:")
                stdscr.refresh()
                language = get_user_input(stdscr)
                if len(language) > 0:
                    Database.create_table(language)
                    language_menu = get_language_menu(Database)
                else:
                    stdscr.clear()
                    stdscr.addstr('Invalid input. Try again.')
                    stdscr.refresh()
                    stdscr.getch()
            else:
                chosen_language = language_menu[language_menu_idx]
                return chosen_language

        print_menu(stdscr, language_menu, language_menu_idx)
        stdscr.refresh()


def start(stdscr, Database, language):
    data = Database.get_data_from_table(language)
    if len(data) == 0:
        stdscr.clear()
        stdscr.addstr('Table is empty. Import data first.')
        return 0
    else:
        df = pd.DataFrame(data)
        while 1:
            pass


def main(stdscr):
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    db = database.Database()

    main_menu_idx = 0
    print_menu(stdscr, MAIN_MENU, main_menu_idx)

    while 1:
        key = stdscr.getch()
        if key in [curses.KEY_UP, ASCII_VIM_KEYS["k"]] and main_menu_idx > 0:
            main_menu_idx -= 1
        elif key in [curses.KEY_DOWN, ASCII_VIM_KEYS["j"]] and main_menu_idx < len(MAIN_MENU)-1:
            main_menu_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()
            stdscr.refresh()

            if MAIN_MENU[main_menu_idx] == 'Exit':
                exit(0)
            elif MAIN_MENU[main_menu_idx] == 'Start':
                language = get_language(stdscr, db)
            elif MAIN_MENU[main_menu_idx] == 'Import Data':
                pass

        print_menu(stdscr, MAIN_MENU, main_menu_idx)
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
