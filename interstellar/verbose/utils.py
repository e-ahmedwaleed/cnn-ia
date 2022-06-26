import sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

enum_table = {}
STANDARD_WIDTH = 12


def print_output(title, content, note=''):
    length = len(title) + 2
    top = "┌"
    if note:
        bot = " │ [" + note + "]\n└"
    else:
        bot = " │\n└"
    for i in range(length):
        top += "─"
        bot += "─"
    top += "┐\n│ "
    bot += "┘\n"
    if content:
        print(top + title + bot + str(content))
    else:
        print(top + title + bot[:-1])


# (1.0, 1.0, ...) -> (1, 1, ...)
def to_ints(floats_tuple):
    ints_list = []
    for n in floats_tuple:
        ints_list.append(int(n))
    return tuple(ints_list)


# "[[2 ,4], [...]]" -> (OX, OC)(...)
def identify_loops_in_list_of_lists(list_of_loops):
    s = ''
    for list_of_loop in list_of_loops:
        t = '('
        for loop in list_of_loop:
            t += str(enum_table[loop]) + ', '
        s += t[:-2] + ')'
    return s


# "(24)(...)" & '(' -> [0, 4, ..]
def find_occurrences(string, char):
    return [i for i, letter in enumerate(string) if letter == char]


# "(24)(...)" -> (OX, OC)(...)
def identify_loops_in_brackets_str(str_of_loops):
    s = ''
    for i in find_occurrences(str_of_loops, '('):
        j = i + 1
        t = '('
        while str_of_loops[j] != ')':
            t += str(enum_table[int(str_of_loops[j])]) + ', '
            j = j + 1
        s += t[:-2] + ')'
    return s
