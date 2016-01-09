import os
import sets
import atexit
import hashlib
import logging
import tempfile
import subprocess
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
            'data_dir': 'data',
            'output': 'hardcopy.pdf',
            'template_vars': {}
        }

    def build(self):
        self.mk_build_dir()
        self.config['template_vars']['segments'] = self.barcodes()
        self.jinja2_render()
        self.pandoc_render()

    def mk_build_dir(self):
        os.mkdir(
            self.config['build_dir'], 0700)
        
        os.chdir(self.config['build_dir'])
        
        os.mkdir(
            self.config['barcode_dir'], 0700)
        
        os.mkdir(
            self.config['src_dir'], 0700)

        os.mkdir(
            self.config['data_dir'], 0700)

    def generate_segments(self):

        data = open(
            os.path.join(
                self.config['data_dir'],
                'data'
            ),
            'w',
            0600
        )

        count = 0
        while True:
            segment = self.config['input'].read(
                self.config['segment_size']
            )
            
            if not segment:
                data.close()
                break
            
            data.write(segment)
            
            with open(
                    os.path.join(
                        self.config['data_dir'],
                        'segment-%02d' % (count)
                    ),
                    'w',
                    0600
            ) as f:
                f.write(segment)
                
            count = count + 1
            
            yield segment

    def barcodes(self, format=''):
        return list(self.generate_barcodes(format=format))
            
    def generate_barcodes(self, format=''):
        filename_format = format or self.config['barcode'] + '-%02d.png'
        
        self.Barcoder = Barcoder(barcode=self.config['barcode'])

        for index,segment in enumerate(self.generate_segments()):
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

        self.config['hardcopy_md'] = os.path.join(
            self.config['src_dir'],
            'hardcopy.md'
        )

        hardcopy_md_f = open(self.config['hardcopy_md'], 'w')
        hardcopy_md_f.write(markdown)
        hardcopy_md_f.close()
        
    def pandoc_render(self):
        try:
            subprocess.check_output(['/usr/bin/pandoc',
                                     '--from',
                                     'markdown+yaml_metadata_block',
                                     '--output',
                                     self.config['output'],
                                     self.config['hardcopy_md']
                                 ],
                                    stderr=subprocess.STDOUT
                                )
        except subprocess.CalledProcessError as e:
            print(e.output)
