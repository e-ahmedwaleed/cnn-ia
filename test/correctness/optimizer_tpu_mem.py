'''
Simple test case for checking get_cost
'''
import unittest
import cnn_mapping as cm 
import numpy as np
class TestOptimizer(unittest.TestCase):

    '''       
    def test_alex_conv2(self):
        capacity_list = [512/2, 131072/2, 2097152*256] 
        access_cost_list = [1, 6, 200] 
        static_cost_list = [0, 0, 0]  
        para_count_list = [192, 1, 1] 

        # {loop: [[order, blocking, partitioning],[],...]}
        #schedule_hint = {cm.le.FX: [[0, 5, 1], None, None], cm.le.IC: [[3, 1, 12], None, None],
        #                 cm.le.FY: [[1, 5, 1], None, None], cm.le.OY: [[5, 1, 1], None, None],
        #                 cm.le.OX: [[4, 1, 1], None, None], cm.le.OC: [[4, 1, 16], None, None],
        #                 cm.le.ON: [[6, 1, 1], None, None]}

        schedule_hint = {cm.le.IC: [[3, None, 12], None, None],
                         cm.le.OC: [[4, None, 16], None, None]}

        resource = cm.Resource(capacity_list, access_cost_list, static_cost_list, para_count_list, 0, [1, 0, 0], [2])
        layer = cm.Layer(48, 256, 28, 28, 5, 5, 1)
        opt_result = cm.optimizer.opt_optimizer(resource, layer, schedule_hint, True)
        level0 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 0)
        level1 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 1)
        level2 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 2)
        level00 = cm.cost_model.get_array_and_curr_level_cost(resource, opt_result[1], layer, 1) - level1
        print level0, level00, level1, level2
        cm.utils.print_loop_nest(opt_result[1])

    ''' 
    def test_alex_conv1(self):
        reg_size = 16
        buffer_size = 16384 
        reg_cost = 0.05
        buffer_cost = 3.84
        capacity_list = [512/2, 131072/2, 2097152*256] #32B, 32KB
        access_cost_list = [1, 6, 200] 
        static_cost_list = [0, 0, 0]  
        para_count_list = [192, 1, 1] 

        # {loop: [[order, blocking, partitioning],[],...]}
        schedule_hint = {cm.le.IC: [[3, 1, 3], None, None],
                         cm.le.OC: [[5, None, 16], None, None],
                         cm.le.ON: [[4, None, 4], None, None]}

        layer = cm.Layer(3, 96, 55, 55, 11, 11, 16, 4, 4)

        energy_list = np.zeros((5,5))
        for x in xrange(0, 5):
            capacity_list[1] = buffer_size * (2**x)
            access_cost_list[1] = buffer_cost * (1.25**x)
            for y in xrange(0, 5):
                capacity_list[0] = reg_size * (2**y)
                access_cost_list[0] = reg_cost * (2**y)
 
                resource = cm.Resource(capacity_list, access_cost_list, static_cost_list, para_count_list, 0, [1, 0, 0], [2])
                opt_result = cm.optimizer.opt_optimizer(resource, layer, schedule_hint, True)
                level0 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 0)
                level1 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 1)
                level2 = cm.cost_model.get_level_cost(resource, opt_result[1], layer, 2)
                level00 = cm.cost_model.get_array_and_curr_level_cost(resource, opt_result[1], layer, 1) - level1
                print level0, level00, level1, level2
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
