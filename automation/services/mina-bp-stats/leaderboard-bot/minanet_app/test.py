import unittest
import numpy as np
from Validation.helper import filter_state_hash_percentage, create_graph
import pandas as pd

class TestingGraphMethods(unittest.TestCase):
    def test_filter_state_hash_single(self):
        master_state_hash = pd.DataFrame([['state_hash_1', 'block_producer_key_1']], columns=['state_hash', 'block_producer_key'])
        output = filter_state_hash_percentage(master_state_hash)
        self.assertEqual(output, ['state_hash_1'])

    def test_filter_state_hash_multi(self):
        master_state_hash = pd.DataFrame([['state_hash_1', 'block_producer_key_1'], ['state_hash_1', 'block_producer_key_2'], ['state_hash_2', 'block_producer_key_3']], columns=['state_hash', 'block_producer_key'])
        output = filter_state_hash_percentage(master_state_hash)
        self.assertEqual(output, ['state_hash_1'])

    # batch weight
    def test_count_number_of_nodes_and_edges(self):
        # current batch that was downloaded
        batch_df = pd.DataFrame([['state_hash_1', 'parent_state_hash_1'], ['state_hash_2', 'parent_state_hash_2']], columns=['state_hash', 'parent_state_hash'])
        # previous_state_hashes with weight
        p_selected_node_df = pd.DataFrame(['parent_state_hash_1'], columns=['state_hash'])
        # filtered_state_hashes  
        c_selected_node =  ['state_hash_1', 'state_hash_2']
        # relations between parents and children, i.e. those previous stte hashes that are parents in this batch.
        p_map = [['parent_state_hash_1', 'state_hash_1']]
        output = create_graph(batch_df, p_selected_node_df, c_selected_node, p_map)
        # total number of nodes is always those in the current batch + those from previous
        self.assertEqual(len(output.nodes), len(batch_df) + len(p_selected_node_df))
        # there are no nodes in the current batch that are also parents of later nodes in the batch (see next test)
        self.assertEqual(len(output.edges), len(p_map))

    def test_count_number_of_nodes_and_edges_nested(self):
        # current batch that was downloaded
        batch_df = pd.DataFrame([['state_hash_1', 'parent_state_hash_1'], ['state_hash_2', 'state_hash_1'], ['state_hash_3', 'state_hash_2']], columns=['state_hash', 'parent_state_hash'])
        # previous_state_hashes with weight
        p_selected_node_df = pd.DataFrame(['parent_state_hash_1'], columns=['state_hash'])
        # filtered_state_hashes  
        c_selected_node =  ['state_hash_1', 'state_hash_2']
        # relations between parents and children, i.e. those previous stte hashes that are parents in this batch.
        p_map = [['parent_state_hash_1', 'state_hash_1']]
        output = create_graph(batch_df, p_selected_node_df, c_selected_node, p_map)
        self.assertEqual(len(output.nodes), len(batch_df) + len(p_selected_node_df))      
        self.assertEqual(len(output.edges), len(p_map) + 2)

    # queue List

    # graph

    # bfs

if __name__ == '__main__':
    unittest.main()