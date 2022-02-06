'''
Simple test case for dataflow exploration
'''

import unittest
import cnn_mapping as cm


class TestDataflow(unittest.TestCase):

    def test_dataflow_explore(self):
        capacity_list = [32, 131072, 2097152]
        access_cost_list = [0.1, 6, 64]
        static_cost_list = [0.2, 32 * 0.2, 4096 * 0.2]
        para_count_list = [12, 1, 1]

        resource = cm.Resource(capacity_list, access_cost_list, static_cost_list, para_count_list, 0, [1, 0, 0], [2])
        layer = cm.Layer(32, 32, 16, 16, 3, 3, 4)

        dataflow_tb = cm.mapping_point_generator.dataflow_exploration(resource, layer, verbose=True)
        print("dataflows:", dataflow_tb)


if __name__ == '__main__':
    unittest.main()
