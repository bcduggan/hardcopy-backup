import hashlib
import logging

logging.basicConfig(level=logging.DEBUG)

class HardcopyBackup(object):

    config = {
        'barcode': 'QR',
        'segment_size': 256,
    }
    
    def __init__(self, input):
        self.config['input'] = input
        return

    def segments(self):
        input = self.config['input']
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
