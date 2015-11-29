import logging
import click
from HardcopyBackup import HardcopyBackup

logging.basicConfig(level=logging.INFO)

CONTEXT_SETTINGS = dict(
    default_map={'backup':
                 {
                     'barcode': 'QR',
                     'to': 'PDF',
                     'segment_size': 512,
                 }
             }
)

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    ## TODO: Load defaults from .ini file
    pass

@cli.command()
@click.option('--barcode', '-b',
              type=click.Choice(['QR', 'DMTX', 'PDF417']))
@click.option('--to', '-t',
              type=click.Choice(['PDF','PS','DOCX','ODT','RTF']))
@click.option('--segment-size', '-s', type=click.INT)
@click.argument('input', type=click.File('rb'))
def backup(*args, **kwargs):
    hc = HardcopyBackup(kwargs['input'], config=kwargs)

    for barcode in hc.generate_barcodes():
        logging.info(barcode['hash'].hexdigest())
        logging.info(barcode['image'])
    return

if __name__ == '__main__':
    cli()

