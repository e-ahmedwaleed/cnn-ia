import verbose.utils as utils

from verbose.utils import STANDARD_WIDTH


def generate_field_row_format(field_function):
    table_height = len(utils.enum_table)
    table_width = len(field_function(0))

    _max = -1
    for i in range(table_height):
        if _max < max(field_function(i)):
            _max = max(field_function(i))

    column_width = max(len(str(int(_max))) + STANDARD_WIDTH / 2, STANDARD_WIDTH)

    row_format = '\t'
    for j in range(table_width):
        row_format += "%-" + str(int(column_width)) + "s "

    return row_format + '%s'


def mapping_config_field(title, field_function):
    table_height = len(utils.enum_table)
    table_width = len(field_function(0))

    table = '  ' + title + '\n'

    row_format = generate_field_row_format(field_function)

    header = ["MEM:"]
    for j in range(table_width):
        header.append("L" + str(j))
    table += (row_format % tuple(header)) + '\n'

    for i in range(table_height):
        row = utils.enum_table[i] + ':'
        table += (row_format % (row, *utils.to_ints(field_function(i)))) + '\n'

    return table


def tabulate_mapping_config(mapping_configuration):
    table = ''
    table += mapping_config_field("Loop temporal blocking (factors)",
                                  mapping_configuration.loop_blocking)
    table += mapping_config_field("Loop spatial partitioning (units)",
                                  mapping_configuration.loop_partitioning)
    table += mapping_config_field("Loop ordering (from the innermost)",
                                  mapping_configuration.loop_order)
    return table[:-1]


def generate_cost_row_format(costs):
    _max = max(costs)
    table_width = len(costs)
    column_width = max(len(str(_max)) + STANDARD_WIDTH / 2, STANDARD_WIDTH)

    row_format = '\t'
    for j in range(table_width + 1):
        row_format += "%-" + str(int(column_width)) + "s "

    return row_format + '%s'


def tabulate_energy_costs(para_index, level_costs):
    table_width = len(level_costs) - len(para_index)
    row_format = generate_cost_row_format(level_costs)

    table = ''

    header = ["MEM:"]
    for j in range(table_width):
        header.append("L" + str(j))
        if j in para_index:
            header.append("L" + str(j) + "-PARA")

    header.append("TOTAL")
    table += (row_format % tuple(header)) + '\n'

    row = 'ENERGY:'
    # last memory level is not checked for invalid_underutilized,
    # memory_partitions[-1] = [None]s leading to level_costs[-1] = 0
    costs = []
    for cost in level_costs:
        if cost:
            costs.append(cost)
        else:
            costs.append("NOT_CHECKED")
    table += (row_format % (row, *costs, sum(level_costs)))

    return table


def schedule_details(loop):
    return "for ( " + loop[0] + ", " + str(int(loop[1])) + "b" + ", " + str(int(loop[2])) + "p )"


def tabulate_loop_blocking(loop_nest):
    table_width = len(loop_nest[0])

    table = ''

    for i in range(table_width):
        i = table_width - i - 1
        taps = '\t'
        table += taps + "MEM - L" + str(i) + ":" + '\n'
        loop_nest[0][i].reverse()
        for loop in loop_nest[0][i]:
            if loop:
                taps += '\t'
                table += taps + schedule_details(loop) + '\n'
        if loop_nest[1][i]:
            table += "\n\t\tspatially unrolled loops: " + utils.identify_loops_in_list_of_lists(loop_nest[1][i]) + '\n'

    return table[:-1] if table[-1] == '\n' else table
