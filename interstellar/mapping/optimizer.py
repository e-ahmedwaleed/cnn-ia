'''
Top level function of optimization framework
'''

from . import cost_model
from . import mapping_point_generator


def opt_optimizer(resource, layer, hint=None, verbose=False):
    '''
    Evaluate the cost of each mapping point,
    record the mapping_point with the smallest cost
    '''

    smallest_cost, best_mapping_point = mapping_point_generator.opt_mapping_point_generator_function(resource, layer,
                                                                                                     hint, verbose)
    # access_list, array_cost = cost_model.get_access(best_mapping_point, layer, resource)

    # total_cost = cost_model.get_cost(resource, best_mapping_point, layer, verbose)
    # assert total_cost == smallest_cost

    if verbose:
        print(smallest_cost)
        print("Best mapping_point: ", best_mapping_point.loop_blockings, best_mapping_point.loop_partitionings,
              best_mapping_point.loop_orders)
    return [smallest_cost, best_mapping_point]  # , access_list]


def optimizer(resource, layer, hint=None, verbose=False):
    smallest_cost = float("inf")
    mp_generator = mapping_point_generator.mapping_point_generator_function(resource, layer, hint, verbose)

    # counter = 0
    for mapping_point in mp_generator:
        # counter += 1
        cost = cost_model.get_cost(resource, mapping_point, layer, verbose)
        # if verbose:
        #    print "Current cost: ", cost
        #     print "Current mapping_point: ", mapping_point.loop_blockings, mapping_point.loop_orders

        if cost < smallest_cost:
            smallest_cost = cost
            best_mapping_point = mapping_point
            if verbose:
                print("Current smallest cost: ", smallest_cost)
                print("Current best mapping_point: ", mapping_point.loop_blockings, mapping_point.loop_orders)
    # print counter

    if verbose:
        print(smallest_cost)
        print("Best mapping_point: ", best_mapping_point.loop_blockings, mapping_point.loop_partitionings,
              best_mapping_point.loop_orders)

    return [smallest_cost, best_mapping_point]
