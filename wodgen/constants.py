SPECIAL_CHARACTERS = {
    '/': 'v',
    '\n': ' ',
    '\r': ' ',
    '\u201c': '',
    '\u201d': '',
    ',': '',
    '\t\r\n': ' ',
    '-': '',
    '"''': '',
}

TIME_MAPPING = {
    1: tuple(range(0, 5)),
    2: tuple(range(5, 15)),
    3: tuple(range(15, 90))
}

