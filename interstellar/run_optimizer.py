import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import numpy as np
import argparse
import time
import cnn_mapping as cm
import cnn_mapping.loop_enum as le

STANDARD_WIDTH = 12


def generate_field_row_format(field_function):
    table_height = le.NUM
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


def to_ints(floats_tuple):
    ints_list = []
    for n in floats_tuple:
        ints_list.append(int(n))
    return tuple(ints_list)


def mapping_config_field(title, field_function):
    table_height = le.NUM
    table_width = len(field_function(0))

    table = '  ' + title + '\n'

    row_format = generate_field_row_format(field_function)

    header = ["MEM:"]
    for j in range(table_width):
        header.append("L" + str(j))
    table += (row_format % tuple(header)) + '\n'

    for i in range(table_height):
        row = le.table[i] + ':'
        table += (row_format % (row, *to_ints(field_function(i)))) + '\n'

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
    table += (row_format % (row, *level_costs, sum(level_costs)))

    return table


def schedule_details(loop):
    return "for ( " + loop[0] + ", " + str(int(loop[1])) + "b" + ", " + str(int(loop[2])) + "p )"


def identify_loops_in_list_of_lists(list_of_loops):
    s = ''
    for list_of_loop in list_of_loops:
        s += str(le.table[list_of_loop[0]]) + ', '
    return s[:-2]


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
            table += "\n\t\tspatially unrolled loops: " + identify_loops_in_list_of_lists(loop_nest[1][i]) + '\n'

    return table


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
    print(top + title + bot + str(content))


def basic_optimizer(arch_info, network_info, schedule_info=None, basic=False, verbose=False):
    # Hardware resource specification
    resource = cm.Resource.arch(arch_info)
    # NN layer specification
    layer = cm.Layer.layer(network_info)
    # Schedule hint specification
    schedule = cm.Schedule.schedule(schedule_info) if schedule_info is not None else None
    # Find the smallest cost mapping configuration.
    opt_result = cm.optimizer.opt_optimizer(resource, layer, schedule)
    # Memory accesses (inputs, outputs, weights, parallel: neighborhood PE) per level.
    level_costs = cm.cost_model.get_level_costs(resource, opt_result[1], layer, verbose)

    if verbose or basic:
        print_output("MAPPING CONFIGURATION", tabulate_mapping_config(opt_result[1]))
        print_output("COST FOR EACH LEVEL", tabulate_energy_costs(resource.para_index, level_costs), "measured in pJ")
        print_output("BEST SCHEDULE", tabulate_loop_blocking(cm.utils.print_loop_nest(opt_result[1])),
                     "b: blocking factor, p: partitioning unit")
    return opt_result[0]


def mem_explore_optimizer(arch_info, network_info, schedule_info, verbose=False):
    assert "explore_points" in arch_info, "missing explore_points in arch file"
    assert "capacity_scale" in arch_info, "missing capacity_scale in arch file"
    assert "access_cost_scale" in arch_info, "missing access_cost_scale in arch file"
    # cwd = os.getcwd()
    # output_filename = os.path.join(cwd, "dataset", network_info['layer_name'] + '_128.csv')
    explore_points = arch_info["explore_points"]
    energy_list = np.zeros(tuple(explore_points))
    summary_array = np.zeros([np.product(explore_points), 12])
    # TODO support more than two levels of explorations
    capacity0 = arch_info["capacity"][0]
    capacity1 = arch_info["capacity"][1]
    cost0 = arch_info["access_cost"][0]
    cost1 = arch_info["access_cost"][1]
    i = 0
    for x in range(explore_points[0]):
        arch_info["capacity"][0] = capacity0 * (arch_info["capacity_scale"][0] ** x)
        arch_info["access_cost"][0] = cost0 * (arch_info["access_cost_scale"][0] ** x)
        for y in range(explore_points[1]):
            # if x == 0 and y < 1:
            #    continue
            arch_info["capacity"][1] = capacity1 * (arch_info["capacity_scale"][1] ** y)
            arch_info["access_cost"][1] = cost1 * (arch_info["access_cost_scale"][1] ** y)
            print(arch_info)
            energy = basic_optimizer(arch_info, network_info, schedule_info, False, verbose)
            energy_list[x][y] = energy
            cur_point = network_info["layer_info"] + arch_info["capacity"][:-1] + [energy]
            summary_array[i] = cur_point
            # np.savetxt(output_filename, summary_array, delimiter=",")
            i += 1

    print(list(energy_list))
    print("optimal energy for all memory systems: ", np.min(np.array(energy_list)))


def find_occurrences(string, char):
    return [i for i, letter in enumerate(string) if letter == char]


def identify_loops_in_brackets_str(str_of_loops):
    s = ''
    for i in find_occurrences(str_of_loops, '('):
        s += str(le.table[int(str_of_loops[i + 1])]) + ', '
    return s[:-2]


def print_tabulated_dataflow_results(dataflow_tb):
    for unrollment in sorted(dataflow_tb):
        title = identify_loops_in_brackets_str(unrollment)
        content = tabulate_mapping_config(dataflow_tb[unrollment][2])
        note = "cost: " + str(dataflow_tb[unrollment][0]) + " pJ, util: " \
               + str(dataflow_tb[unrollment][1] * 100) + "%"
        print_output(title, content, note)
    print()


def print_tabulated_best_schedules(dataflow_tb):
    best_cost = best_util = None
    for unrollment in dataflow_tb:
        if best_cost:
            if dataflow_tb[unrollment][0] < dataflow_tb[best_cost][0]:
                best_cost = unrollment
            if dataflow_tb[unrollment][1] > dataflow_tb[best_util][1]:
                best_util = unrollment
        else:
            best_cost = best_util = unrollment

    print_output("BEST COST", tabulate_loop_blocking(cm.utils.print_loop_nest(dataflow_tb[best_cost][2])),
                 "b: blocking factor, p: partitioning unit")
    print_output("BEST UTILIZATION", tabulate_loop_blocking(cm.utils.print_loop_nest(dataflow_tb[best_util][2])),
                 "b: blocking factor, p: partitioning unit")


def dataflow_explore_optimizer(arch_info, network_info, file_name, verbose=False):
    # Ahmed - TODO: compare and fix other assertions
    assert any(n > 1 for n in arch_info["parallel_count"]), \
        "parallel count has to be more than 1 for dataflow exploration"

    # Hardware resource specification
    resource = cm.Resource.arch(arch_info)
    # NN layer specification
    layer = cm.Layer.layer(network_info)
    # Generate unrolled loops mapping configurations table
    dataflow_tb = cm.mapping_point_generator.dataflow_exploration(resource, layer, file_name)

    if verbose:
        print_tabulated_dataflow_results(dataflow_tb)
        print_tabulated_best_schedules(dataflow_tb)

    return dataflow_tb


# -v -s ./samples/schedule/eyeriss_alex_conv3.json mem_explore ./samples/arch/3_level_mem_explore.json ./samples/layer/mlp_fc3_batch16.json
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=["basic", "mem_explore", "dataflow_explore"], help="optimizer type")
    parser.add_argument("arch", help="architecture specification")
    parser.add_argument("network", help="network specification")
    parser.add_argument("-s", "--schedule", help="restriction of the schedule space")
    parser.add_argument("-n", "--name", default="dataflow_table", help="name for the dumped pickle file")
    parser.add_argument("-v", "--verbose", action='count', help="verbosity")
    args = parser.parse_args()

    start = time.time()
    i_arch_info, i_network_info, i_schedule_info = cm.extract_input.extract_info(args)
    if args.type == "basic":
        basic_optimizer(i_arch_info, i_network_info, i_schedule_info, True, args.verbose)
    elif args.type == "mem_explore":
        mem_explore_optimizer(i_arch_info, i_network_info, i_schedule_info, args.verbose)
    elif args.type == "dataflow_explore":
        dataflow_explore_optimizer(i_arch_info, i_network_info, args.name, args.verbose)
    end = time.time()
    print("elapsed time: ", (end - start))
