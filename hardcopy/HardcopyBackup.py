import os
import sets
import atexit
import hashlib
import logging
import tempfile
from Barcoder import Barcoder

logging.basicConfig(level=logging.INFO)

class HardcopyBackup(object):

    def __init__(self, input, barcode, to, segment_size, backup_name, build_dir=''):
        self.config = {
            'input': input,
            'barcode': barcode,
            'to': to,
            'segment_size': segment_size,
            'backup_name': backup_name,
            'build_dir': build_dir or tempfile.mkdtemp(prefix='hardcopy-'),
        }

        self.mk_build_dir()

    def mk_build_dir(self):
        os.makedirs(os.path.join(
            self.config['build_dir'],
            self.config['backup_name'],
            'barcodes'), mode=0700)
        
    def segments(self):
        input = self.config['input']
        size = self.config['segment_size']
        
        while True:
            segment = input.read(size)
            if not segment:
                break
            yield segment

    def generate_barcodes(self, format=''):
        filename_format = format or self.config['barcode'] + '-%02d.' + self.config['to'].lower()
        
        self.Barcoder = Barcoder(barcode=self.config['barcode'])

        logging.error(self.config['backup_name'])
        barcode_dir = os.path.join(
            self.config['build_dir'],
            self.config['backup_name'],
            'barcodes')

        for index,segment in enumerate(self.segments()):
            segment_hash = hashlib.sha256()
            segment_hash.update(segment)

            self.Barcoder.encode(segment,
                                 os.path.join(
                                     barcode_dir,
                                     filename_format % (index)
                                     )
                                 )
            
            yield {
                'barcode_filename': filename_format % (index),
                'hash': segment_hash,
            }
