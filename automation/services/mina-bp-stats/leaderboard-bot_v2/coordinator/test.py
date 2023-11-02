from datetime import datetime
from helper import pullFileNames
import unittest

class TestingHelpers(unittest.TestCase):
    def testFilePullSmallRange(self):
        start_time = datetime.strptime('2023-08-03T16:31:58Z',"%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.strptime('2023-08-03T16:31:59Z', "%Y-%m-%dT%H:%M:%SZ")
        filtered_list = pullFileNames(start_time, end_time, "block-bucket-name", True)
        self.assertEqual(len(filtered_list), 1)

    def testFilePullLargeRange(self):
        start_time = datetime.strptime('2023-08-03T16:32:00Z',"%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.strptime('2023-08-03T16:33:59Z', "%Y-%m-%dT%H:%M:%SZ")
        filtered_list = pullFileNames(start_time, end_time, "block-bucket-name", True)
        self.assertEqual(len(filtered_list), 11)

if __name__ == '__main__':
    unittest.main()