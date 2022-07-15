from . import mapping as cm
from .verbose import utils as utils
from .verbose import dataflow as df_utils
from .reports import dataflow as dataflow_report

utils.enum_table = cm.loop_enum.table


def dataflow_explore_optimizer(arch_info, network_info, verbose=False, report_path=None):
    assert any(n > 1 for n in arch_info["parallel_count"]), \
        "parallel count has to be more than 1 for dataflow exploration"

    # Hardware resource specification
    resource = cm.Resource.arch(arch_info)
    # NN layer specification
    layer = cm.Layer.layer(network_info)
    # Generate unrolled loops mapping configurations table
    dataflow_tb = cm.mapping_point_generator.dataflow_exploration(resource, layer)

    if verbose:
        df_utils.print_tabulated_dataflow_results(dataflow_tb)
        df_utils.print_tabulated_best_schedules(cm.utils.print_loop_nest, dataflow_tb)

    if report_path:
        dataflow_report.generate(cm.utils.print_loop_nest, dataflow_tb, arch_info, network_info, report_path)

    return dataflow_tb
