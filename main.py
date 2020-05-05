import screen
import curses
import database
import random
from os import listdir, getcwd
from os.path import isfile, join


def create_language_menu(Database):
    language_menu = []

    languages = Database.tables
    if len(languages) > 0:
        for language in languages:
            language_menu.append(language)

    language_menu.append('Exit')

    return language_menu


def create_csv_file_menu():
    dir_list = listdir(getcwd())
    file_menu = [f for f in dir_list if isfile(
        join(getcwd(), f)) and f[-3:] == 'csv']
    file_menu.append('Exit')
    return file_menu


def import_data(Database, table_name, file_name):
    Database.import_data_from_csv(table_name, file_name)


def start(stdscr, Database, language):
    flashcards = Database.get_data_from_table(language)
    if len(flashcards) == 0:
        message = 'No flashcards available...'
        screen.print_message(stdscr, message)
        return 0
    else:
        learning_batches = [[], [], [], []]
        for flashcard in flashcards:
            if flashcard[-1] == 0:
                learning_batches[0].append(flashcard)
            elif flashcard[-1] == 3:
                learning_batches[1].append(flashcard)
            elif flashcard[-1] == 2:
                learning_batches[2].append(flashcard)
            elif flashcard[-1] == 1:
                learning_batches[3].append(flashcard)
            else:
                exit(1)
        for i, learning_batch in enumerate(learning_batches):
            while len(learning_batch) > 0:
                screen.print_message(stdscr, f'Batch: {i+1}')
                flashcard = list(learning_batch[random.randint(
                    0, len(learning_batch) - 1)])
                screen.print_message(stdscr, flashcard[0])
                answer = screen.get_keyboard_input(stdscr)
                if answer == flashcard[1] and i != len(learning_batches) - 1:
                    learning_batch.pop(learning_batch.index(tuple(flashcard)))
                    flashcard[2] = 1
                    learning_batches[-1].append(tuple(flashcard))
                    message = 'That was correct!'
                    screen.print_message(stdscr, message)
                elif answer == flashcard[1] and i == len(learning_batches) - 1:
                    message = 'That was correct!'
                    screen.print_message(stdscr, message)
                else:
                    message = 'That wasn\'t correct! The correct answer is {}'.format(
                        flashcard[1])
                    screen.print_message(stdscr, message)


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    db = database.Database()

    while 1:
        main_menu = ['Start', 'Import Data', 'Exit']
        main_menu_idx = 0

        screen.print_menu(stdscr, main_menu, main_menu_idx)
        chosen_menu_item = screen.get_menu_item(
            stdscr, main_menu, main_menu_idx)
        if chosen_menu_item == 'Exit':
            exit(0)
        elif chosen_menu_item == 'Import Data':
            language_menu = create_language_menu(db)
            language_menu_idx = 0
            message = 'Please choose a language...'
            screen.print_message(stdscr, message)
            screen.print_menu(stdscr, language_menu, language_menu_idx)
            chosen_language = screen.get_menu_item(
                stdscr, language_menu, language_menu_idx)
            if chosen_language == 'Exit':
                continue
            file_menu = create_csv_file_menu()
            file_menu_idx = 0
            message = 'Please choose a file...'
            screen.print_message(stdscr, message)
            screen.print_menu(stdscr, file_menu, file_menu_idx)
            chosen_file = screen.get_menu_item(
                stdscr, file_menu, file_menu_idx)
            if chosen_file == 'Exit':
                continue
            import_data(db, chosen_language, chosen_file)
            screen.print_message(stdscr, 'Import was successful.')
        elif chosen_menu_item == 'Start':
            language_menu = create_language_menu(db)
            new_language_option = 'Create New Language'
            language_menu.insert(0, new_language_option)
            language_menu_idx = 0
            message = 'Please choose a language...'
            screen.print_message(stdscr, message)
            screen.print_menu(stdscr, language_menu, language_menu_idx)
            chosen_language = screen.get_menu_item(
                stdscr, language_menu, language_menu_idx)
            if chosen_language == 'Exit':
                continue
            elif chosen_language == new_language_option:
                message = 'Enter new language...'
                screen.print_message(stdscr, message)
                new_language = screen.get_keyboard_input(stdscr)
                new_language = new_language.strip()
                db.create_table(new_language)
                message = 'New language successfully created.'
                screen.print_message(stdscr, message)
            else:
                start(stdscr, db, chosen_language)


if __name__ == "__main__":
    curses.wrapper(main)
