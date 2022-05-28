import interstellar.cnn_mapping.loop_enum as le

STANDARD_WIDTH = 12


def to_ints(floats_tuple):
    ints_list = []
    for n in floats_tuple:
        ints_list.append(int(n))
    return tuple(ints_list)


def identify_loops_in_list_of_lists(list_of_loops):
    s = ''
    for list_of_loop in list_of_loops:
        s += str(le.table[list_of_loop[0]]) + ', '
    return s[:-2]


def find_occurrences(string, char):
    return [i for i, letter in enumerate(string) if letter == char]


def identify_loops_in_brackets_str(str_of_loops):
    s = ''
    for i in find_occurrences(str_of_loops, '('):
        s += str(le.table[int(str_of_loops[i + 1])]) + ', '
    return s[:-2]


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
