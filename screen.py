import curses

ASCII_VIM_KEYS = {
    'j': 106,
    'k': 107
}

ASCII_KEYS = {
    0:     'NUL',
    1:     'SOH',
    2:     'STX',
    3:     'ETX',
    4:     'EOT',
    5:     'ENQ',
    6:     'ACK',
    7:     'BEL',
    8:     'BS',
    9:     'HT',
    10:    'LF',
    11:    'VT',
    12:    'FF',
    13:    'CR',
    14:    'SO',
    15:    'SI',
    16:    'DLE',
    17:    'DC1',
    18:    'DC2',
    19:    'DC3',
    20:    'DC4',
    21:    'NAK',
    22:    'SYN',
    23:    'ETB',
    24:    'CAN',
    25:    'EM',
    26:    'SUB',
    27:    'ESC',
    28:    'FS',
    29:    'GS',
    30:    'RS',
    31:    'US',
    32:    ' ',
    33:    '!',
    34:    '"',
    35:    '#',
    36:    '$',
    37:    '%',
    38:    '&',
    39: "'",
    40: '(',
    41: ')',
    42: '*',
    43: '+',
    44: ',',
    45: '-',
    46: '.',
    47: '/',
    48: '0',
    49: '1',
    50: '2',
    51: '3',
    52: '4',
    53: '5',
    54: '6',
    55: '7',
    56: '8',
    57: '9',
    58: ':',
    59: ';',
    60: '<',
    61: '=',
    62: '>',
    63: '?',
    64: '@',
    65: 'A',
    66: 'B',
    67: 'C',
    68: 'D',
    69: 'E',
    70: 'F',
    71: 'G',
    72: 'H',
    73: 'I',
    74: 'J',
    75: 'K',
    76: 'L',
    77: 'M',
    78: 'N',
    79: 'O',
    80: 'P',
    81: 'Q',
    82: 'R',
    83: 'S',
    84: 'T',
    85: 'U',
    86: 'V',
    87: 'W',
    88: 'X',
    89: 'Y',
    90: 'Z',
    91: '[',
    92: '\\',
    93: ']',
    94: '^',
    95: '_',
    96: '`',
    97: 'a',
    98: 'b',
    99: 'c',
    100: 'd',
    101: 'e',
    102: 'f',
    103: 'g',
    104: 'h',
    105: 'i',
    106: 'j',
    107: 'k',
    108: 'l',
    109: 'm',
    110: 'n',
    111: 'o',
    112: 'p',
    113: 'q',
    114: 'r',
    115: 's',
    116: 't',
    117: 'u',
    118: 'v',
    119: 'w',
    120: 'x',
    121: 'y',
    122: 'z',
    123: '{',
    124: '|',
    125: '}',
    126: '~',
    127: 'BSP'
}


def print_message(stdscr, message):
    h, w = stdscr.getmaxyx()

    stdscr.clear()

    x = w//2 - len(message)//2
    y = h//2

    stdscr.addstr(y, x, message)
    stdscr.refresh()
    stdscr.getch()


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


def get_menu_item(stdscr, menu, selected_row_idx):
    while 1:
        key = stdscr.getch()
        if key in [curses.KEY_UP, ASCII_VIM_KEYS["k"]] and selected_row_idx > 0:
            selected_row_idx -= 1
        elif key in [curses.KEY_DOWN, ASCII_VIM_KEYS["j"]] and selected_row_idx < len(menu)-1:
            selected_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()
            stdscr.refresh()
            return menu[selected_row_idx]

        print_menu(stdscr, menu, selected_row_idx)


def get_keyboard_input(stdscr):
    stdscr.clear()
    stdscr.addstr('Your answer: ')
    curses.curs_set(1)
    stdscr.refresh()
    keyboard_input = ''
    while 1:
        key = stdscr.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:
            curses.curs_set(0)
            break
        elif len(keyboard_input) > 0 and (key == curses.KEY_BACKSPACE or key == 127):
            keyboard_input = keyboard_input[:-1]
            stdscr.clear()
            stdscr.addstr('Your answer: ')
            stdscr.addstr(keyboard_input)
            stdscr.refresh()
        else:
            keyboard_input = keyboard_input + ASCII_KEYS[key]
            stdscr.addstr(ASCII_KEYS[key])
            stdscr.refresh()
    return keyboard_input
