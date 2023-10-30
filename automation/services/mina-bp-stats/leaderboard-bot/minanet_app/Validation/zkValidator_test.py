from multiprocessing_copy import processing_batch_files, get_validate_state_hash
import unittest
import os

class TestingZkValidator(unittest.TestCase):
    def test_get_validate_state_hash(self):
        file_list = ['2023-10-26T00_01_06Z-B62qoWzouroXrwjqeV8RxHHRULUaxxeN1fh247EFz2R7uGJerAF4TSn.json']
        combine_list=[]
        output = get_validate_state_hash(file_list,combine_list)
        self.assertEqual(output, [])
        
if __name__ == '__main__':
    unittest.main()
# ZkDofMkCMu23hRuPTDviE8ej5pDAbyS24qw7NFbQ4mS9H5FUc4