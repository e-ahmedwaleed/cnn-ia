'''
Top level function of optimization framework
'''
import mapping_point_generator
import cost_model

import loop_enum as le
import buffer_enum as be 

def opt_optimizer(resource, layer, hint=None, verbose=False):
    '''
    Evaluate the cost of each mapping point,
    record the mapping_point with the smallest cost
    '''
    valid = True
    if hint is not None and hint.partition_loops is None:
        valid = cost_model.valid_dataflow(resource, hint.schedule_hint)
    assert valid == True, "Specified schedule doesn't satisfy the utilization threshold, please check partitioning_size"

    smallest_cost, perf, best_mapping_point = mapping_point_generator.opt_mapping_point_generator_function(resource, layer, hint, verbose)
    total_cost = cost_model.get_cost(resource, best_mapping_point, layer, verbose)
  
    if verbose:
        print "Optimal energy (pJ): ", smallest_cost
        print "Runtime (cycles):", perf
        print "Best mapping_point: ", best_mapping_point.loop_blockings, best_mapping_point.loop_partitionings, best_mapping_point.loop_orders
    return [smallest_cost, best_mapping_point]
 

