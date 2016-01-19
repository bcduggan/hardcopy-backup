import re
import sys
import click
import pexpect
import hashlib
import logging
import xmltodict

logging.basicConfig(level=logging.INFO)

class HardcopyRestore(object):

    def __init__(self, barcode, output):
        self.get_zbarcam()
        return

    def get_zbarcam(self):
        self.zbarcam = pexpect.spawn('/usr/bin/zbarcam' +
                                     ' --quiet' +
                                     ' --xml' +
                                     ' --prescale=320x240',
                                     timeout=3600)

        first_line = re.compile(
            '<barcodes xmlns=\'http://zbar\.sourceforge\.net/2008/barcode\'>' +
            '<source device=\'(?P<device>.*)\'>\r\n'
        )

        if self.zbarcam.expect([first_line, pexpect.TIMEOUT]) == 1:
            logging.error('Unexpected zbarcam output.')
            exit(1)

    def get_barcode_data(self):
    # Sample zbarcam output:
    #<barcodes xmlns='http://zbar.sourceforge.net/2008/barcode'><source device=''>
    #<index num='273'>
    #<symbol type='QR-Code' quality='1'><data><![CDATA[http://streetsense.org/]]></data></symbol>
    #</index>
    #</source></barcodes>
    
        while self.zbarcam.expect(['</index>', pexpect.EOF]) == 0:
            yield xmltodict.parse(
                self.zbarcam.before + '</index>'
            )
            
    def restore(self):
        data = ''
        data_hash = hashlib.sha1()

        for barcode_data in self.get_barcode_data():
            segment_hash = hashlib.sha1()
            
            data_hash.update(barcode_data['index']['symbol']['data'])
            segment_hash.update(barcode_data['index']['symbol']['data'])

            click.echo('\r', nl=False, err=True)
            click.echo('Segment sha1sum:   ' + segment_hash.hexdigest(),
                       err=True)
            click.echo('Full data sha1sum: ' + data_hash.hexdigest(),
                       nl=False, err=True)

            sys.stdout.write(barcode_data['index']['symbol']['data'])

        click.echo('', err=True)
        self.zbarcam.terminate()
        return
