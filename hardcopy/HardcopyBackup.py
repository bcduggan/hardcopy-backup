import os
import sets
import atexit
import hashlib
import logging
import tempfile
from jinja2 import Environment, PackageLoader
from Barcoder import Barcoder

logging.basicConfig(level=logging.INFO)

class HardcopyBackup(object):

    def __init__(self, input, barcode, to, segment_size, build_dir):
        self.config = {
            'input': input,
            'barcode': barcode,
            'to': to,
            'segment_size': segment_size,
            'build_dir': build_dir,
            'barcode_dir': 'barcodes',
            'src_dir': 'src',
            'template_vars': {}
        }

    def build(self):
        self.mk_build_dir()
        self.config['template_vars']['segments'] = self.barcodes()
        self.jinja2_render()

    def mk_build_dir(self):
        os.mkdir(
            self.config['build_dir'], 0700)
        
        os.chdir(self.config['build_dir'])
        
        os.mkdir(
            self.config['barcode_dir'], 0700)
        
        os.mkdir(
            self.config['src_dir'], 0700)
        
    def segments(self):
        input = self.config['input']
        size = self.config['segment_size']
        
        while True:
            segment = input.read(size)
            if not segment:
                break
            yield segment

    def barcodes(self, format=''):
        return list(self.generate_barcodes(format=format))
            
    def generate_barcodes(self, format=''):
        filename_format = format or self.config['barcode'] + '-%02d.png'
        
        self.Barcoder = Barcoder(barcode=self.config['barcode'])

        for index,segment in enumerate(self.segments()):
            segment_hash = hashlib.sha256()
            segment_hash.update(segment)

            barcode_path = os.path.join(
                self.config['barcode_dir'],
                filename_format % (index)
            )


            self.Barcoder.encode(segment, barcode_path)
            
            yield {
                'barcode_filename': barcode_path,
                'hash': segment_hash,
            }

    def jinja2_render(self):
        jenv = Environment(
            loader=PackageLoader(__name__, 'templates'))

        template = jenv.get_template('hardcopy.md.j2')

        markdown = template.render(self.config['template_vars'])

        hardcopy_md = os.path.join(
            self.config['src_dir'], 'hardcopy.md')

        hardcopy_md_f = open(hardcopy_md, 'w')
        hardcopy_md_f.write(markdown)
        hardcopy_md_f.close()
