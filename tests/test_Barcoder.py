import os
import unittest
import logging
from hardcopy import Barcoder
from hardcopy import HardcopyError

logging.basicConfig(level=logging.DEBUG)

class TestBarcoder(unittest.TestCase):

    def setUp(self):
        self.barcoder = Barcoder('/tmp')

    def test_init_without_config(self):
        self.assertIsInstance(self.barcoder, Barcoder)

    def test_get_const(self):
        self.assertIsNotNone(self.barcoder.get_const('max_size'))

    def test_get_max_size(self):
        self.assertIsNotNone(self.barcoder.get_max_size())

    def test_check_config_Good_Barcode(self):
        self.assertIsNone(self.barcoder.check_config())

    def test_check_config_Bad_Barcode(self):
        self.barcoder.config['barcode'] = 'UPC'
        self.assertRaises(HardcopyError, self.barcoder.check_config)
    
    def test_init_with_config(self):
        self.barcoder = Barcoder('/tmp', barcode='QR')
        self.assertIsInstance(self.barcoder, Barcoder)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
