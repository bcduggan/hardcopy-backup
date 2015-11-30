import os
import atexit
import qrtools
import logging
import tempfile
from HardcopyError import HardcopyError

logging.basicConfig(level=logging.DEBUG)

class Barcoder():

    defaults = {
        'barcode': 'QR',
    }

    const = {
        'QR': {
            'max_size': 2953
        }
    }

    def get_const(self, name):
        return self.const[self.config['barcode']][name]

    def get_max_size(self):
        return self.get_const('max_size')

    def check_config(self):
        if self.config['barcode'] not in self.const.keys():
            raise HardcopyError('Barcode type %s is not supported.' % (self.config['barcode']))
    
    def build_config(self, build_dir, config={}):
        self.config = {}
        self.config.update(self.defaults)
        self.config.update(config)

        self.config['build_dir'] = os.path.join(build_dir, 'barcodes')

        self.check_config()

    def setup_encoder(self):
        if self.config['barcode'] == 'QR':
            ## TODO: Move off qrtools.
            ## qrtools generates temporary files insecurely.
            ## As-yet unknown whether text decoding through zbar will work
            ## because qrtools prioritizes mobile devices.
            ## Can I fix these with my own decorators?
            import qrtools
            self.QR = qrtools.QR(data_type=u'text')
            # Undo qrtools' insecure temp file creation
            self.QR.destroy()
            self.QR.directory = self.config['build_dir']

    def __init__(self, build_dir, **kwargs):
        self.build_config(build_dir, kwargs)
        self.setup_encoder()

    def encode(self, data):
        if len(data) > self.get_max_size():
            raise HardcopyError('%s barcodes cannot contain more than %d bits of data.'
                                % (self.config['barcode'], self.get_max_size()))
        
        if type(data) != type(''):
            logging.debug(type(data))
            raise HardcopyError('Only unicode string data are supported at this time.')

        if self.config['barcode'] == 'QR':
            self.QR.data = data
            self.QR.encode()
            filename = self.QR.filename

        return(filename)
