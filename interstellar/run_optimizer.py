import time
import argparse
import numpy as np
import mapping as cm
import verbose.dataflow as df_utils
import verbose.loop_blocking as lb_utils
import verbose.memory_explore as me_utils
import report_generation.basic_report as report
import verbose.utils as utils

utils.enum_table = cm.loop_enum.table


def basic_optimizer(arch_info, network_info, schedule_info=None, verbose=False):
    # Hardware resource specification
    resource = cm.Resource.arch(arch_info)
    # NN layer specification
    layer = cm.Layer.layer(network_info)
    # Schedule hint specification
    schedule = cm.Schedule.schedule(schedule_info) if schedule_info is not None else None
    # Find the smallest cost mapping configuration
    opt_result = cm.optimizer.opt_optimizer(resource, layer, schedule)

    if verbose:
        # Memory accesses (inputs, outputs, weights, parallel: neighborhood PE) per level
        level_costs = cm.cost_model.get_level_costs(resource, opt_result[1], layer, verbose)

        utils.print_output("MAPPING CONFIGURATION", lb_utils.tabulate_mapping_config(opt_result[1]))
        utils.print_output("COST FOR EACH LEVEL", lb_utils.tabulate_energy_costs(resource.para_index, level_costs),
                           "measured in pJ")
        utils.print_output("SCHEDULE", lb_utils.tabulate_loop_blocking(cm.utils.print_loop_nest(opt_result[1])),
                           "b: blocking factor, p: partitioning unit")
        report.generate_basic(opt_result[1],
                              level_costs, resource.para_index,
                              cm.utils.print_loop_nest(opt_result[1]))
    return opt_result


def mem_explore_optimizer(arch_info, network_info, schedule_info, verbose=False):
    assert "explore_points" in arch_info, "missing explore_points in arch file"
    assert "capacity_scale" in arch_info, "missing capacity_scale in arch file"
    assert "access_cost_scale" in arch_info, "missing access_cost_scale in arch file"

    # Memory exploration dimensions
    explore_points = arch_info["explore_points"]
    # Number of memory levels * 2 + cost column
    columns = len(arch_info["capacity"]) * 2 + 1
    # Initialize exploration table
    exploration_tb = np.zeros([np.product(explore_points), columns])

    # TODO support more than two levels of explorations
    capacity1 = arch_info["capacity"][1]
    capacity0 = arch_info["capacity"][0]
    cost1 = arch_info["access_cost"][1]
    cost0 = arch_info["access_cost"][0]

    i = 0
    for y in range(explore_points[1]):
        arch_info["capacity"][1] = capacity1 * (arch_info["capacity_scale"][1] ** y)
        arch_info["access_cost"][1] = cost1 * (arch_info["access_cost_scale"][1] ** y)
        for x in range(explore_points[0]):
            arch_info["capacity"][0] = capacity0 * (arch_info["capacity_scale"][0] ** x)
            arch_info["access_cost"][0] = cost0 * (arch_info["access_cost_scale"][0] ** x)
            try:
                energy = basic_optimizer(arch_info, network_info, schedule_info)[0]
                exploration_tb[i] = arch_info["capacity"] + arch_info["access_cost"] + [energy]
            except AssertionError as err:
                if err.args[0] == "No valid mapping point found.":
                    exploration_tb[i] = arch_info["capacity"] + arch_info["access_cost"] + [float("inf")]
                else:
                    raise
            i += 1

    if verbose:
        utils.print_output("EXPLORATION TABLE", me_utils.tabulate_exploration_table(exploration_tb))
        content, note = me_utils.tabulate_optimal_arch(exploration_tb)
        utils.print_output("OPTIMAL COST", content, note)

    return exploration_tb


def dataflow_explore_optimizer(arch_info, network_info, file_name, verbose=False):
    # TODO: compare and fix other assertions
    # Many dataflow explorations failed because of the wrong assertion from before
    # assert arch_info["parallel_count"][0] > 1, \
    assert any(n > 1 for n in arch_info["parallel_count"]), \
        "parallel count has to be more than 1 for dataflow exploration"

    # Hardware resource specification
    resource = cm.Resource.arch(arch_info)
    # NN layer specification
    layer = cm.Layer.layer(network_info)
    # Generate unrolled loops mapping configurations table
    dataflow_tb = cm.mapping_point_generator.dataflow_exploration(resource, layer, file_name)

    if verbose:
        df_utils.print_tabulated_dataflow_results(dataflow_tb)
        df_utils.print_tabulated_best_schedules(cm.utils.print_loop_nest, dataflow_tb)

    return dataflow_tb


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
        basic_optimizer(i_arch_info, i_network_info, i_schedule_info, args.verbose)
    elif args.type == "mem_explore":
        mem_explore_optimizer(i_arch_info, i_network_info, i_schedule_info, args.verbose)
    elif args.type == "dataflow_explore":
        dataflow_explore_optimizer(i_arch_info, i_network_info, args.name, args.verbose)
    end = time.time()
    utils.print_output("ELAPSED TIME", "", str(end - start) + " sec")
