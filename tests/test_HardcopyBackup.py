import os
import unittest
import logging
from hardcopy import HardcopyBackup

logging.basicConfig(level=logging.DEBUG)

class TestHardcopyBackupClass(unittest.TestCase):

    def test_init_without_config(self):
        config = {
            'barcode': 'QR',
            'to': 'PDF',
            'segment_size': 512,
        }
        
        hc = HardcopyBackup('input')
        self.assertEqual(config, hc.config)

    def test_init_with_config(self):
        config = {'barcode': 'PDF417'}

        result = {
            'barcode': 'PDF417',
            'to': 'PDF',
            'segment_size': 512,
        }

        hc = HardcopyBackup('input', config)
        self.assertEqual(result, hc.config)

    def test_segments(self):
        size = 0
        with open('tests/fixtures/gpg.key.asc') as data:
            hc = HardcopyBackup(data)
            for segment in hc.segments():
                if len(segment) > size:
                    size = len(segment)
        self.assertLessEqual(size, hc.config['segment_size'])

if __name__ == '__main__':
    unittest.main()


