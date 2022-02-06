'''
Simple test case for checking mapping_point_generator
'''
import unittest
import cnn_mapping as cm


class TestCostModel(unittest.TestCase):

    def test_simple(self):
        order_generator = cm.mapping_point_generator.order_generator_function(3, 2)
        self.assertEqual(next(order_generator), [(0, 0), (1, 1), (2, 2)])
        self.assertEqual(next(order_generator), [(0, 0), (1, 2), (2, 1)])
        self.assertEqual(next(order_generator), [(0, 1), (1, 0), (2, 2)])
        self.assertEqual(next(order_generator), [(0, 1), (1, 2), (2, 0)])

    def test_tile(self):
        result_permutations = cm.mapping_point_generator.loop_tile(6, 3)
        self.assertEqual(len(result_permutations), 9)
        result_permutations = cm.mapping_point_generator.loop_tile(12, 3)
        self.assertEqual(len(result_permutations), 18)

    def test_tile_hint(self):
        loop_hint = [[0, 3, 1], None, None]
        result_permutations = cm.mapping_point_generator.loop_tile(6, 3, loop_hint)
        self.assertEqual(len(result_permutations), 2)
        result_permutations = cm.mapping_point_generator.loop_tile(12, 3, loop_hint)
        self.assertEqual(len(result_permutations), 3)
        loop_hint = [[0, 3, 4], None, None]
        result_permutations = cm.mapping_point_generator.loop_tile(96, 3, loop_hint)
        self.assertEqual(len(result_permutations), 4)

    def test_tile_generator_hint4(self):
        # {loop: [level, order, blocking, partitioning]}
        schedule_hint = {cm.le.FX: [None, [0, 3, 1], None],
                         cm.le.IC: [None, [1, 1, 4], None], cm.le.OC: [None, [2, 1, 4], None]}

        tile_per = []
        cm.mapping_point_generator.loop_tile_with_hint(tile_per, 32, 3, schedule_hint[cm.le.IC])
        self.assertEqual(tile_per[0], [8, 4, 1])
        self.assertEqual(tile_per[1], [1, 4, 8])
        self.assertEqual(tile_per[2], [2, 4, 4])
        self.assertEqual(tile_per[3], [4, 4, 2])

        tile_per = []
        cm.mapping_point_generator.loop_tile_with_hint(tile_per, 42, 3, schedule_hint[cm.le.OC])
        self.assertEqual(tile_per[0], [1, 4, 11])
        self.assertEqual(tile_per[1], [11, 4, 1])

        tile_per = []
        schedule_hint = {cm.le.IC: [None, [1, 2, 4], None, None], cm.le.OC: [None, [2, 1, 4], None, None]}
        cm.mapping_point_generator.loop_tile_with_hint(tile_per, 64, 4, schedule_hint[cm.le.IC])
        self.assertEqual(tile_per[0], [8, 8, 1, 1])
        self.assertEqual(tile_per[1], [1, 8, 8, 1])
        self.assertEqual(tile_per[3], [1, 8, 2, 4])
        self.assertEqual(tile_per[9], [4, 8, 2, 1])

        ''' TODO: UNCOMMENT
        tile_per = []
        schedule_hint = {cm.le.IC: [[1, 1, 4], None, None], cm.le.OC: [[2, 1, 4], None, None]}
        cm.mapping_point_generator.loop_tile_with_hint(tile_per, 64, 3, schedule_hint[cm.le.IC])
        self.assertEqual(tile_per[0], [4, 16, 1])
        self.assertEqual(tile_per[2], [4, 2, 8])
        self.assertEqual(tile_per[4], [4, 8, 2])

        tile_per = []
        schedule_hint = {cm.le.IC: [[0, None, 4], None, None], cm.le.OC: [[2, 1, 4], None, None]}
        cm.mapping_point_generator.loop_tile_with_hint(tile_per, 64, 3, schedule_hint[cm.le.IC])
        self.assertEqual(tile_per[0], [64, 1, 1])
        self.assertEqual(tile_per[3], [4, 2, 8])
        self.assertEqual(tile_per[14], [16, 4, 1])

        tile_per = []
        schedule_hint = {cm.le.IC: [None, [0, None, 4], None], cm.le.OC: [None, [2, 1, 4], None]}
        cm.mapping_point_generator.loop_tile_with_hint(tile_per, 64, 3, schedule_hint[cm.le.IC])
        self.assertEqual(tile_per[0], [16, 4, 1])
        self.assertEqual(tile_per[4], [1, 8, 8])
        self.assertEqual(tile_per[14], [8, 4, 2])
        '''

    def test_tile_generator_hint5(self):
        capacity_list = [32, 512, 2097152]
        access_cost_list = [1, 6, 64]
        static_cost_list = [0.2, 32 * 0.2, 4096 * 0.2]
        para_count_list = [1, 16, 1]

        # {loop: [level, order, blocking, partitioning]}
        schedule_hint = {cm.le.FX: [None, [0, 3, 1], None],
                         cm.le.IC: [None, [1, None, 4], None], cm.le.OC: [None, [2, None, 4], None]}

        resource = cm.Resource(capacity_list, access_cost_list, static_cost_list, para_count_list, 0, [0, 1, 0], [2])
        layer = cm.Layer(64, 32, 8, 8, 3, 3, 1)
        # tile_per = []
        # cm.mapping_point_generator.loop_tile_with_hint(tile_per, 32, 3, schedule_hint[cm.le.IC])
        # for tile in tile_per:

    #     print tile
    # tile_generator = cm.mapping_point_generator.blocking_partitioning_generator_function_with_hint(resource, layer, schedule_hint)
    # for tile in tile_generator:
    #    print  tile


if __name__ == '__main__':
    unittest.main()
