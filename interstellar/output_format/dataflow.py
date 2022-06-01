import output_format.utils as utils

from output_format.loop_blocking import tabulate_mapping_config, tabulate_loop_blocking


def print_tabulated_dataflow_results(dataflow_tb):
    for unrollment in sorted(dataflow_tb):
        title = utils.identify_loops_in_brackets_str(unrollment)
        content = tabulate_mapping_config(dataflow_tb[unrollment][2])
        note = "cost: " + str(dataflow_tb[unrollment][0]) + " pJ, utilization: " \
               + str(dataflow_tb[unrollment][1] * 100) + "%"
        utils.print_output(title, content, note)


def print_tabulated_best_schedules(loop_nest, dataflow_tb):
    best_cost = best_util = None
    for unrollment in dataflow_tb:
        if best_cost:
            if dataflow_tb[unrollment][0] < dataflow_tb[best_cost][0]:
                best_cost = unrollment
            if dataflow_tb[unrollment][1] > dataflow_tb[best_util][1]:
                best_util = unrollment
        else:
            best_cost = best_util = unrollment

    utils.print_output("OPTIMAL COST", tabulate_loop_blocking(loop_nest(dataflow_tb[best_cost][2])),
                       "b: blocking factor, p: partitioning unit")
    utils.print_output("OPTIMAL UTILIZATION", tabulate_loop_blocking(loop_nest(dataflow_tb[best_util][2])),
                       "b: blocking factor, p: partitioning unit")