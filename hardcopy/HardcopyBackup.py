import hashlib
import logging

logging.basicConfig(level=logging.DEBUG)

class HardcopyBackup(object):

    def __init__(self, input, config={}):
        self.input = input
        self.config = {
            'barcode': 'QR',
            'to': 'PDF',
            'segment_size': 512,
        }
        self.config.update(config)

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

    def encode(self, segment):
        return(segment)
    
    def generate_barcodes(self):
        for segment in self.segments():
            segment_hash = hashlib.sha256()
            segment_hash.update(segment)
            
            yield {
                'image': self.encode(segment),
                'hash': segment_hash,
            }
