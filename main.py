# Time to test
import os
import unittest
import pandas as pd
from GetInfo import write_file


class TestTradeProcessing(unittest.TestCase):
    def setUp(self):
        self.in_path = os.path.realpath('SampleInput.csv')
        self.out_path = os.path.realpath('SampleOutput.csv')
        self.test_path = 'test.csv'

        if not os.path.exists(self.in_path):
            self.fail(f"Missing input file: {self.in_path}")

        write_file(self.in_path, self.test_path)

        self.in_data = pd.read_csv(self.in_path)
        self.out_data = pd.read_csv(self.out_path)
        self.test_data = pd.read_csv(self.test_path)

    def test_check_output(self):
        self.assertTrue(self.out_data.compare(self.test_data).empty, "Generated output does not match expected output")

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)


if __name__ == '__main__':
    unittest.main()