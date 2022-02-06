'''
Simple test case for checking get_cost
'''
import unittest
import numpy as np
import cnn_mapping as cm 

class TestOptimizer(unittest.TestCase):

    '''         
    def test_alex_conv2(self):
        reg0_size = 4
        reg1_size = 32
        reg0_cost = 0.1/8
        reg1_cost = 0.1
        capacity_list = [64/2, 512/2, 131072/4, 2097152*256] #32B, 32KB
        access_cost_list = [0.1, 1, 6/1.25, 200]
        static_cost_list = [0, 0, 0, 0]
        para_count_list = [1, 140, 1, 1] 


        schedule_hint = {cm.le.FY: [None, [2, 1, 5], None, None], cm.le.OY: [None, [3, 1, 28], None, None]}

        layer = cm.Layer(48, 256, 28, 28, 5, 5, 16)

        energy_list = np.zeros((4,4))
        for x in xrange(0, 4):
            capacity_list[1] = reg1_size * (2**x)
            access_cost_list[1] = reg1_cost * (2**x)
            for y in xrange(0, 4):
                capacity_list[0] = reg0_size * (2**y)
                access_cost_list[0] = reg0_cost * (2**y)

                resource = cm.Resource(capacity_list, access_cost_list, static_cost_list, para_count_list, 0, [0, 1, 0, 0], [2])
                opt_result = cm.optimizer.opt_optimizer(resource, layer, schedule_hint, True)
                level0 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 0)
                level1 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 1)
                level2 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 2)
                level3 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 3)
                level00 = cm.cost_model.get_array_and_curr_level_cost(resource, opt_result[1], layer, 2) - level2
                print level0, level1, level00, level2, level3
                cm.utils.print_loop_nest(opt_result[1])
                energy_list[x][y] = opt_result[0]
        print list(energy_list)


    def test_alex_conv3(self):
        reg0_size = 4
        reg1_size = 32
        reg0_cost = 0.1/8
        reg1_cost = 0.1
        capacity_list = [64/2, 512/2, 131072/2, 2097152*256] #32B, 32KB
        access_cost_list = [0.1, 1, 6*1.25, 200]
        static_cost_list = [0, 0, 0, 0]
        para_count_list = [1, 156, 1, 1]

        # {loop: [[order, blocking, partitioning],[],...]}
        schedule_hint = {cm.le.FY: [None, [2, 1, 3], None, None], cm.le.OY: [None, [3, 1, 13], None, None],
                         cm.le.OC: [None, [4, None, 4], None, None]}

        layer = cm.Layer(256, 384, 13, 13, 3, 3, 1)

        energy_list = np.zeros((4,3))
        for x in xrange(0, 4):
            capacity_list[1] = reg1_size * (2**x)
            access_cost_list[1] = reg1_cost * (2**x)
            for y in xrange(0, 3):
                capacity_list[0] = reg0_size * (2**y)
                access_cost_list[0] = reg0_cost * (2**y)

                resource = cm.Resource(capacity_list, access_cost_list, static_cost_list, para_count_list, 0, [0, 1, 0, 0], [2])
                opt_result = cm.optimizer.opt_optimizer(resource, layer, schedule_hint, True)
                level0 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 0)
                level1 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 1)
                level2 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 2)
                level3 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 3)
                level00 = cm.cost_model.get_array_and_curr_level_cost(resource, opt_result[1], layer, 2) - level2
                print level0, level1, level00, level2, level3
                cm.utils.print_loop_nest(opt_result[1])
                energy_list[x][y] = opt_result[0]
        print list(energy_list)
    '''

    def test_alex_conv1(self):
        reg0_size = 4
        reg1_size = 32
        reg0_cost = 0.1/8
        reg1_cost = 0.1
        capacity_list = [64/2, 512/2, 131072/2, 2097152*256] #32B, 32KB
        access_cost_list = [0.1, 1, 6, 200]
        static_cost_list = [0, 0, 0, 0]
        para_count_list = [1, 156, 1, 1]

        # {loop: [[order, blocking, partitioning],[],...]}
        schedule_hint = {cm.le.FY: [None, [2, 1, 11], None, None], cm.le.OY: [None, [3, 1, 3], None, None],
                         cm.le.IC: [None, [4, None, 2], None, None]}

        layer = cm.Layer(3, 96, 55, 55, 11, 11, 16, 4, 4)

        energy_list = np.zeros((4,4))
        for x in xrange(0, 4):
            capacity_list[1] = reg1_size * (2**x)
            access_cost_list[1] = reg1_cost * (2**x)
            for y in xrange(0, 4):
                capacity_list[0] = reg0_size * (2**y)
                access_cost_list[0] = reg0_cost * (2**y)

                resource = cm.Resource(capacity_list, access_cost_list, static_cost_list, para_count_list, 0, [0, 1, 0, 0], [2])
                opt_result = cm.optimizer.opt_optimizer(resource, layer, schedule_hint, True)
                level0 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 0)
                level1 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 1)
                level2 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 2)
                level3 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 3)
                level00 = cm.cost_model.get_array_and_curr_level_cost(resource, opt_result[1], layer, 2) - level2
                print level0, level1, level00, level2, level3
                cm.utils.print_loop_nest(opt_result[1])
                energy_list[x][y] = opt_result[0]
        print list(energy_list)


    ''' 
    def test_vgg_conv2(self):
        capacity_list = [512/2, 131072/2, 2097152*1024] 
        access_cost_list = [1, 6, 200] 
        static_cost_list = [0, 0, 0]  
        para_count_list = [256, 1, 1] 

        # {loop: [[order, blocking, partitioning],[],...]}
        schedule_hint = {cm.le.IC: [[3, None, 16], None, None],
                         cm.le.OC: [[4, None, 16], None, None]}

        resource = cm.Resource(capacity_list, access_cost_list, static_cost_list, para_count_list, 0, [1, 0, 0], [2])
        layer = cm.Layer(64, 64, 224, 224, 3, 3, 1)
        opt_result = cm.optimizer.opt_optimizer(resource, layer, schedule_hint, True)
        level0 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 0)
        level1 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 1)
        level2 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 2)
        level00 = cm.cost_model.get_array_and_curr_level_cost(resource, opt_result[1], layer, 1) - level1
        print level0, level00, level1, level2
        cm.utils.print_loop_nest(opt_result[1]) 
    
    def test_vgg_conv12(self):
        capacity_list = [512/2, 131072/2, 2097152*1024]
        access_cost_list = [1, 6, 200]
        static_cost_list = [0, 0, 0]
        para_count_list = [256, 1, 1]

        # {loop: [[order, blocking, partitioning],[],...]}
        schedule_hint = {cm.le.IC: [[3, None, 16], None, None],
                         cm.le.OC: [[4, None, 16], None, None]}

        resource = cm.Resource(capacity_list, access_cost_list, static_cost_list, para_count_list, 0, [1, 0, 0], [2])
        layer = cm.Layer(512, 512, 14, 14, 3, 3, 1)
        opt_result = cm.optimizer.opt_optimizer(resource, layer, schedule_hint, True)
        level0 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 0)
        level1 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 1)
        level2 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 2)
        level00 = cm.cost_model.get_array_and_curr_level_cost(resource, opt_result[1], layer, 1) - level1
        print level0, level00, level1, level2
        cm.utils.print_loop_nest(opt_result[1])
     
    '''

if __name__ == '__main__':
    unittest.main()
