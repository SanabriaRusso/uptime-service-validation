from multiprocessing_copy import processing_batch_files, get_validate_state_hash
import unittest
import os

class TestingZkValidator(unittest.TestCase):
    def test_get_validate_state_hash(self):
        print ("New file", os.path.join(os.path.dirname(__file__), "test_data"))
        file_list = ['blocks-Y6uq5BokFR7SaDjxzNsYyp6bk21sib5FN51fKRThxTMgQKM4gF.dat']
        combine_list=[]
        output = get_validate_state_hash(file_list,combine_list)
        self.assertEqual(output, [])
        
if __name__ == '__main__':
    unittest.main()
