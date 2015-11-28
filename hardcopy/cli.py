import logging
import click
from HardcopyBackup import HardcopyBackup

logging.basicConfig(level=logging.DEBUG)

@click.command()
@click.option('--barcode', '-b', default='QR',
              type=click.Choice(['QR', 'DMTX', 'PDF417']))
@click.option('--to', '-t', default='PDF',
              type=click.Choice(['PDF','PS','DOCX','ODT','RTF']))
@click.argument('input', type=click.File('rb'))
#@click.argument('output', type=click.Path(exists=False), required=True)
@click.pass_context
def main(ctx, *args, **kwargs):
    hc = HardcopyBackup(kwargs['input'])

    for barcode in hc.generate_barcodes():
        logging.debug(barcode['hash'].hexdigest())

    return

if __name__ == '__main__':
    main()

