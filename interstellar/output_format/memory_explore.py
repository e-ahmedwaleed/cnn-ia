import numpy as np

from output_format.loop_blocking import generate_cost_row_format


def identify_exploration_table_row(exploration_tb, index):
    mem_levels_count = int(np.floor(len(exploration_tb[0]) / 2))

    capacity = exploration_tb[index, 0:mem_levels_count]
    access_cost = exploration_tb[index, mem_levels_count:2 * mem_levels_count]
    cost = exploration_tb[index, 2 * mem_levels_count]

    return capacity, access_cost, cost


def tabulate_exploration_table_row(capacity, access_cost=None, cost=0, header_row=False):
    table_width = len(capacity)
    row_format = generate_cost_row_format([*capacity, *capacity[:-1]])

    table = ''

    if header_row:
        header = []
        for j in range(table_width):
            header.append("L" + str(j) + "-SIZE")
            header.append("L" + str(j) + "-COST")
        header.append("TOTAL")

        table += (row_format % tuple(header)) + '\n'
    else:
        row = []
        for j in range(table_width):
            row.append(capacity[j])
            row.append(access_cost[j])
        row.append(cost)

        table += (row_format % tuple(row)) + '\n'

    return table


def tabulate_exploration_table(exploration_tb):
    capacity, _, _ = identify_exploration_table_row(exploration_tb, 0)
    table = tabulate_exploration_table_row(capacity, header_row=True)

    for i in range(len(exploration_tb)):
        capacity, access_cost, cost = identify_exploration_table_row(exploration_tb, i)
        table += tabulate_exploration_table_row(capacity, access_cost, cost)

    return table[:-1]


def tabulate_memory_arch(capacity, access_cost):
    table_width = len(capacity)
    row_format = generate_cost_row_format(capacity)[:-3]

    table = ''

    header = ["MEM:"]
    for j in range(table_width):
        header.append("L" + str(j))

    table += (row_format % tuple(header)) + '\n'

    row = 'SIZE:'
    table += (row_format % (row, *capacity)) + '\n'

    row = 'COST:'
    table += (row_format % (row, *access_cost))

    return table


def tabulate_optimal_arch(exploration_tb):
    min_cost_index = np.argmin(np.array(exploration_tb[:, -1]))

    capacity, access_cost, cost = identify_exploration_table_row(exploration_tb, min_cost_index)
    arch = tabulate_memory_arch(capacity, access_cost)

    return arch, str(cost) + " pJ"
