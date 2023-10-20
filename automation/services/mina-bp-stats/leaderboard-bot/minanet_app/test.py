import unittest
import numpy as np
from Validation.helper import filter_state_hash_percentage
import pandas as pd

class TestingGraphmethods(unittest.TestCase):
    def test_filter_state_hash(self):
        master_state_hash = pd.DataFrame([['dhdhdhdh', 'hfhf']], columns=['state_hash', 'block_producer_key'])
        output = filter_state_hash_percentage(master_state_hash)
        self.assertEqual(output, [])

if __name__ == '__main__':
    unittest.main()