import re
import pexpect
import hashlib
import logging

logging.basicConfig(level=logging.INFO)

class HardcopyRestore(object):

    def __init__(self, barcode, output):
        self.get_zbarcam()
        return

    def get_zbarcam(self):
        self.zbarcam = pexpect.spawn('/usr/bin/zbarcam --xml --prescale=32x240',
                                     timeout=3600)

    def get_barcode_data(self):
    # Sample zbarcam output:
    #<barcodes xmlns='http://zbar.sourceforge.net/2008/barcode'><source device=''>
    #<index num='273'>
    #<symbol type='QR-Code' quality='1'><data><![CDATA[http://streetsense.org/]]></data></symbol>
    #</index>
    #</source></barcodes>

        xmldata = re.compile(
            '<index num=\'(?P<index>\d+)\'>(\r\n)*' +
            '<symbol type=\'(?P<type>.+)\' quality=\'(?P<quality>\d+)\'>(\r\n)*' +
            '<data>(\r\n)*' +
            '<!\[CDATA\[(?P<data>.*)\]\]>(\r\n)*' +
            '</data>(\r\n)*' +
            '</symbol>\r\n' +
            '</index>'
        )

        while self.zbarcam.expect([xmldata, pexpect.EOF]) == 0:
            yield self.zbarcam.match.groupdict()

    def restore(self):
        data = ''
        data_hash = hashlib.sha1()
        
        for barcode_data in self.get_barcode_data():
            print('HELO')
            segment_hash = hashlib.sha1()

            data_hash.update(barcode_data['data'])
            segment_hash.update(barcode_data['data'])
            data = data + barcode_data['data']
            
            print('Segment sha1sum: ' + segment_hash.hexdigest() )
            print('Full data sha1sum: ' + data_hash.hexdigest() )

        self.zbarcam.terminate()
        print(data)
        return
