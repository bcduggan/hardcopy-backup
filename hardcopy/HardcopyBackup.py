import os
import atexit
import qrtools
import hashlib
import logging
import tempfile
from Barcoder import Barcoder

logging.basicConfig(level=logging.INFO)

class HardcopyBackup(object):

    defaults = {
        'barcode': 'QR',
        'to': 'PDF',
        'segment_size': 512,
    }

    def secure_rm_rf(self, dir):
        for (dirpath, dirnames, filenames) in os.walk(dir):
            for filename in filenames:
                os.remove(os.path.join(dirpath,filename))
        os.rmdir(dir)

    def build_config(self, config={}):
        # If user did not configure a build directory, securely remove
        # the build directory at the at exit.
        if not config.has_key('build_dir'):
            # tempfile prepends relative path with '/tmp/'
            build_dir = tempfile.mkdtemp(prefix='hardcopy-')
            atexit.register(self.secure_rm_rf, build_dir)
            self.defaults['build_dir'] = build_dir
        
        self.config = {}
        self.config.update(self.defaults)
        self.config.update(config)
        
    def __init__(self, input, **kwargs):
        self.input = input
        self.build_config(kwargs)
        logging.debug(self.config)
        return

    def segments(self):
        input = self.input
        size = self.config['segment_size']
        
        while True:
            segment = input.read(size)
            if not segment:
                break
            yield segment

    def generate_barcodes(self):
        self.Barcoder = Barcoder(self.config['build_dir'],
                                 barcode=self.config['barcode'])
        for segment in self.segments():
            segment_hash = hashlib.sha256()
            segment_hash.update(segment)
            
            yield {
                'image': self.Barcoder.encode(segment),
                'hash': segment_hash,
            }
