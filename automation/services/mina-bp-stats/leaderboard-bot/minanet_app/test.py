import unittest
import numpy as np
from Validation.helper import filter_state_hash_percentage
import pandas as pd

class TestingGraphmethods(unittest.TestCase):
    def test_filter_state_hash_single(self):
        master_state_hash = pd.DataFrame([['statehash1', 'block_producer_key_1']], columns=['state_hash', 'block_producer_key'])
        output = filter_state_hash_percentage(master_state_hash)
        self.assertEqual(output, ['statehash1'])

    def test_filter_state_hash_multi(self):
        master_state_hash = pd.DataFrame([['statehash1', 'block_producer_key_1'], ['statehash1', 'block_producer_key_2'], ['statehash2', 'block_producer_key_3']], columns=['state_hash', 'block_producer_key'])
        output = filter_state_hash_percentage(master_state_hash)
        self.assertEqual(output, ['statehash1'])

    # batch weight

    # queue List

    # graph

if __name__ == '__main__':
    unittest.main()