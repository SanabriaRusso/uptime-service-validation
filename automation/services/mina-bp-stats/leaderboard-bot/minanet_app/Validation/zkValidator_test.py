from multiprocessing_copy import processing_batch_files, get_validate_state_hash
import unittest
import os

class TestingZkValidator(unittest.TestCase):
    def test_get_validate_state_hash(self):
        print ("New file", os.path.join(os.path.dirname(__file__), "test_data"))
        file_list = ['2021-08-25T18:51:45Z-B62qrQiw9JhUumq457sMxicgQ94Z1WD9JChzJu19kBE8Szb5T8tcUAC.json']
        combine_list=[]
        output = get_validate_state_hash(file_list,combine_list)
        self.assertEqual(output, [])
        
if __name__ == '__main__':
    unittest.main()
# ZkDofMkCMu23hRuPTDviE8ej5pDAbyS24qw7NFbQ4mS9H5FUc4