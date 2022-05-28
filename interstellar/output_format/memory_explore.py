import numpy as np

from interstellar.output_format.loop_blocking import generate_cost_row_format


def tabulate_memory_arch(capacity, access_cost):
    table_width = len(capacity)
    row_format = generate_cost_row_format(capacity)[:-3]

    table = ''

    header = ["MEM:"]
    for j in range(table_width):
        header.append("L" + str(j))

    table += (row_format % tuple(header)) + '\n'

    row = 'CAPACITY:'
    table += (row_format % (row, *capacity)) + '\n'

    row = 'ACCESS_COST:'
    table += (row_format % (row, *access_cost))

    return table


def tabulate_optimal_arch(exploration_tb):
    mem_levels_count = int(np.floor(len(exploration_tb[0]) / 2))
    min_cost_index = np.argmin(np.array(exploration_tb[:, -1]))

    capacity = exploration_tb[min_cost_index, 0:mem_levels_count]
    access_cost = exploration_tb[min_cost_index, mem_levels_count:2 * mem_levels_count]

    arch = tabulate_memory_arch(capacity, access_cost)
    cost = str(exploration_tb[min_cost_index, 2 * mem_levels_count]) + " pJ"

    return arch, cost
