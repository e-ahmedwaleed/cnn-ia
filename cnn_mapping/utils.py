import cnn_mapping.loop_enum as le
import cnn_mapping.buffer_enum as be


def print_loop_nest(point):
    loop_orders = list(zip(*point.loop_orders))
    loop_blockings = list(zip(*point.loop_blockings))
    loop_partitionings = list(zip(*point.loop_partitionings))
    para_dims = point.para_loop_dim
    num_level = len(loop_orders)
    order_lists = []
    for level in range(num_level):
        order_list = [None] * le.NUM
        for order in range(le.NUM):
            if loop_blockings[level][order] != 1 or loop_partitionings[level][order] != 1:
                order_list[loop_orders[level][order]] = (le.table[order],
                                                         loop_blockings[level][order],
                                                         loop_partitionings[level][order])

        order_lists.append(order_list)

    print(order_lists, para_dims)
