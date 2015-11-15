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

    def process_data(self):
        base_png = os.path.join(self.img_d, 'segment-%d.png')
        
        data = subprocess.check_output(self.config['command'], shell=True)
        segment_size = 512

        full_hash = hashlib.sha256()
        full_hash.update(data)
        self.config['hexdigest'] = full_hash.hexdigest()
    
        segments = []

        # DEBUG
        test_hash = hashlib.sha256()

        for i in range(0,len(data),segment_size):
            segment = data[i:i+segment_size]
            hash = hashlib.sha256()
            hash.update(segment)
            
            #DEBUG
            test_hash.update(segment)

            segment_png = base_png % (i/segment_size)

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

            segments.append({'data': segment,
                             'hexdigest': hash.hexdigest(),
                             'segment_png': segment_png,})
            
            #print(segments[-1]['hash'])

        # DEBUG
        assert test_hash.hexdigest() == self.config['hexdigest']

        self.config['segments'] = segments
        self.config['barcode_count'] = len(segments)
        
        dt = datetime.datetime.utcnow()
        self.config['creation_date'] = dt

    def render_hardcopy(self):
        loader = FileSystemLoader(os.getcwd())

        #jenv = Environment(loader=loader,
        #                   line_statement_prefix='/',
        #                   line_comment_prefix='//')
        jenv = Environment(loader=loader)

        template = jenv.get_template('hardcopy.md.j2')

        print template.render(self.config)

def parse_config():
        with open('config.yml') as config_f:
            config = yaml.load(config_f)
        return config
            
def main():
    config = parse_config()

    #j2_config = process_datum(config[0])

    hc = HardCopy(config[0])
    hc.process_data()
    hc.render_hardcopy()
    
    return

if __name__ == '__main__':
    main()
