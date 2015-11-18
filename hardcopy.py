#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import hashlib
import datetime
import qrencode
import subprocess
from jinja2 import Environment, FileSystemLoader

class HardCopy():

    def __init__(self, config):
        self.config = config
        
        self.build_d = os.path.join(os.getcwd(), 'build')
        self.img_d = os.path.join(self.build_d, 'img')
        try:
            os.mkdir(self.build_d)
        except OSError as e:
            if e.errno == 17:
                pass
        try:
            os.mkdir(self.img_d)
        except OSError as e:
            if e.errno == 17:
                pass


    def qrencode(self, segment, segment_png):
        qrencode = subprocess.Popen(['qrencode',
                                     '--level=%s' % ('L'),
                                     '--type=%s' % ('PNG'),
                                     '--output=%s' % (segment_png)],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    cwd=os.getcwd())
            
        qrencode_result = qrencode.communicate(input=segment)
        
        if qrencode.returncode != 0:
            raise('Could not generate barcode: %s' % (qrencode_result.stderr))

        return
            
    def process_data(self):
        segment_size = 512
        self.data = subprocess.check_output(self.config['command'], shell=True)

        segment_count = len(self.data)/segment_size + 1
        zeropad = segment_count / 10 + 1
        
        base_png = os.path.join(self.img_d, 'segment-%0' + str(zeropad) + 'd.png')
     
        full_hash = hashlib.sha256()
        full_hash.update(self.data)
        self.config['hexdigest'] = full_hash.hexdigest()
    
        segments = []

        # DEBUG
        test_hash = hashlib.sha256()

        for i in range(0,len(self.data),segment_size):
            segment = self.data[i:i+segment_size]
            hash = hashlib.sha256()
            hash.update(segment)
            
            #DEBUG
            test_hash.update(segment)

            segment_png = base_png % (i/segment_size+1)

            self.qrencode(segment, segment_png)

            segments.append({'data': segment,
                             'hexdigest': hash.hexdigest(),
                             'segment_png': segment_png,})
            
        # DEBUG
        assert test_hash.hexdigest() == self.config['hexdigest']

        self.config['segments'] = segments
        self.config['barcode_count'] = len(segments)
        
        dt = datetime.datetime.utcnow()
        self.config['creation_date'] = dt

    def jinja2_render(self):
        loader = FileSystemLoader(os.getcwd())

        jenv = Environment(loader=loader)

        template = jenv.get_template('hardcopy.md.j2')

        self.markdown = template.render(self.config)

        self.hardcopy_md = os.path.join(self.build_d, 'hardcopy.md')
        
        hardcopy_md_f = open(self.hardcopy_md, 'w')
        hardcopy_md_f.write(self.markdown)
        hardcopy_md_f.close()

    def pandoc_render(self):
        self.hardcopy_pdf = os.path.join(self.build_d, 'hardcopy.pdf')

        try:
            subprocess.check_output(['/usr/bin/pandoc',
                                     '--from',
                                     'markdown+yaml_metadata_block',
                                     '--output',
                                     self.hardcopy_pdf,
                                     self.hardcopy_md], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            print(e.output)
           
def parse_config():
        with open('config.yml') as config_f:
            config = yaml.load(config_f)
        return config
            
def main():
    config = parse_config()

    hc = HardCopy(config[0])
    hc.process_data()
    hc.jinja2_render()
    hc.pandoc_render()

    return

if __name__ == '__main__':
    main()
