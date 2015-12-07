import os
import atexit
import logging
import tempfile
import subprocess
from HardcopyError import HardcopyError

logging.basicConfig(level=logging.DEBUG)

class Barcoder():

    const = {
        'QR': {
            'max_size': 2953
        }
    }

    def __init__(self, barcode, image_format='PNG', error_correction='L'):
        self.config = { 'barcode': barcode,
                        'image_format': image_format,
                        'error_correction': error_correction, }
    
    def get_const(self, name):
        return self.const[self.config['barcode']][name]

    def get_max_size(self):
        return self.get_const('max_size')

    def check_config(self):
        if self.config['barcode'] not in self.const.keys():
            raise HardcopyError('Barcode type %s is not supported.' % (self.config['barcode']))
    
    def build_config(self, **kwargs):
        self.config = {}
        self.config.update(self.defaults)
        self.config.update(kwargs)
        self.check_config()

    def qrencode(self, data, filename, image_format, error_correction):
        qrencode = subprocess.Popen(['qrencode',
                                     '--level=%s' % (error_correction),
                                     '--type=%s' % (image_format),
                                     '--output=%s' % (filename)],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    cwd=os.getcwd())

        # Returns (stdout, stderr)
        qrencode_result = qrencode.communicate(input=data)

        if qrencode.returncode != 0:
            raise(HardcopyError(
                'Could not generate barcode: %s' % (qrencode_result[1])))
        return


    def encode(self, data, filename):
        if len(data) > self.get_max_size():
            raise HardcopyError('%s barcodes cannot contain more than %d bits of data.'
                                % (self.config['barcode'], self.get_max_size()))
        
        if self.config['barcode'] == 'QR':
            self.qrencode(data, filename,
                          self.config['image_format'],
                          self.config['error_correction'])
        else:
            raise(HardcopyError('Barcode type %s is not supported.' % (barcode)))
        
        return
