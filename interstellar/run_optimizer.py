import time
import argparse
import numpy as np
import mapping as cm
import verbose.utils as utils
import verbose.dataflow as df_utils
import verbose.loop_blocking as lb_utils
import verbose.memory_explore as me_utils
import reports.basic_report as basic_report
import reports.memory_report as memory_report
import reports.dataflow_report as dataflow_report


utils.enum_table = cm.loop_enum.table


def basic_optimizer(arch_info, network_info, schedule_info=None, verbose=False, reports=False):
    # Hardware resource specification
    resource = cm.Resource.arch(arch_info)
    # NN layer specification
    layer = cm.Layer.layer(network_info)
    # Schedule hint specification
    schedule = cm.Schedule.schedule(schedule_info) if schedule_info is not None else None
    # Find the smallest cost mapping configuration
    opt_result = cm.optimizer.opt_optimizer(resource, layer, schedule)
    # Memory accesses (inputs, outputs, weights, parallel: neighborhood PE) per level
    level_costs = cm.cost_model.get_level_costs(resource, opt_result[1], layer, verbose)

    if verbose:
        utils.print_output("MAPPING CONFIGURATION", lb_utils.tabulate_mapping_config(opt_result[1]))
        utils.print_output("COST FOR EACH LEVEL", lb_utils.tabulate_energy_costs(resource.para_index, level_costs),
                           "measured in pJ")
        utils.print_output("SCHEDULE", lb_utils.tabulate_loop_blocking(cm.utils.print_loop_nest(opt_result[1])),
                           "b: blocking factor, p: partitioning unit")

    if reports:
        basic_report.generate_basic(opt_result[1],
                                    level_costs, resource.para_index,
                                    cm.utils.print_loop_nest(opt_result[1]),
                                    i_arch_info, i_network_info, i_schedule_info)

    return opt_result


def mem_explore_optimizer(arch_info, network_info, schedule_info, verbose=False, reports=False):
    assert "explore_points" in arch_info, "missing explore_points in arch file"
    assert "capacity_scale" in arch_info, "missing capacity_scale in arch file"
    assert "access_cost_scale" in arch_info, "missing access_cost_scale in arch file"

    # Memory exploration dimensions
    explore_points = arch_info["explore_points"]
    # Number of memory levels * 2 + cost column
    columns = len(arch_info["capacity"]) * 2 + 1
    # Initialize exploration table
    exploration_tb = np.zeros([np.product(explore_points), columns])
    mem_levels = arch_info["mem_levels"]
    capacities = []
    costs = []
    for index in range(mem_levels):
        capacities.append(arch_info["capacity"][index])
        costs.append(arch_info["access_cost"][index])

    i = 0
    ind = 1
    ind2 = 1

    if mem_levels >= 2:
        ind2 = explore_points[1]
    if mem_levels >= 3:
        ind = explore_points[2]

    for z in range(ind):
        if mem_levels >= 3:
            arch_info["capacity"][2] = capacities[2] * (arch_info["capacity_scale"][2] ** z)
            arch_info["access_cost"][2] = costs[2] * (arch_info["access_cost_scale"][2] ** z)
        for y in range(ind2):
            if mem_levels >= 2:
                arch_info["capacity"][1] = capacities[1] * (arch_info["capacity_scale"][1] ** y)
                arch_info["access_cost"][1] = costs[1] * (arch_info["access_cost_scale"][1] ** y)
            for x in range(explore_points[0]):
                arch_info["capacity"][0] = capacities[0] * (arch_info["capacity_scale"][0] ** x)
                arch_info["access_cost"][0] = costs[0] * (arch_info["access_cost_scale"][0] ** x)
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

    if reports:
        pos = []
        for index in range(min(mem_levels, len(explore_points), 3)):
            if explore_points[index] != 1:
                pos.append(index)

        memory_report.generate(exploration_tb, pos, arch_info, network_info)

    return exploration_tb


def dataflow_explore_optimizer(arch_info, network_info, file_name, verbose=False, reports=False):
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

    if reports:
        dataflow_report.generate(cm.utils.print_loop_nest, dataflow_tb, arch_info, network_info)

    return dataflow_tb


# TODO: more to be done for reports when gui is ready
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=["basic", "mem_explore", "dataflow_explore"], help="optimizer type")
    parser.add_argument("arch", help="architecture specification")
    parser.add_argument("network", help="network specification")
    parser.add_argument("-s", "--schedule", help="restriction of the schedule space")
    parser.add_argument("-n", "--name", default="dataflow_table", help="name for the dumped pickle file")
    parser.add_argument("-v", "--verbose", action='count', help="verbosity")
    parser.add_argument("-r", "--report", action='count', help="summary report")
    args = parser.parse_args()

    start = time.time()
    i_arch_info, i_network_info, i_schedule_info = cm.extract_input.extract_info(args)
    if args.type == "basic":
        basic_optimizer(i_arch_info, i_network_info, i_schedule_info, args.verbose, args.report)
    elif args.type == "mem_explore":
        mem_explore_optimizer(i_arch_info, i_network_info, i_schedule_info, args.verbose, args.report)
    elif args.type == "dataflow_explore":
        dataflow_explore_optimizer(i_arch_info, i_network_info, args.name, args.verbose, args.report)
    end = time.time()

    if args.verbose:
        utils.print_output("ELAPSED TIME", "", str(end - start) + " sec")
