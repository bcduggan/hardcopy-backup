import os
import click
import logging
import tempfile
from pkg_resources import resource_string
from HardcopyBackup import HardcopyBackup

logging.basicConfig(level=logging.INFO)

#CONTEXT_SETTINGS = dict(
#    default_map={'backup':
#                 {
#                     'barcode': 'QR',
#                     'to': 'PDF',
#                     'segment_size': 512,
#                 }
#             }
#)

#@click.group(context_settings=CONTEXT_SETTINGS)
@click.group()
def cli():
    ## TODO: Load defaults from .ini file
    pass

@cli.command()
def debug():
    #cfg = resource_string(__name__, 'hardcopy.cfg')
    #print(cfg)
    print(os.path.curdir)
    return

@cli.command()
@click.option('--barcode', '-b',
              type=click.Choice(['QR', 'DMTX', 'PDF417']),
              default='QR')
@click.option('--to', '-t',
              type=click.Choice(['PDF','PS','DOCX','ODT','RTF']),
              default='PDF')
@click.option('--segment-size', '-s', type=click.INT, default=512)
@click.option('--build_dir', '-d',
                type=click.Path(exists=False,
                                file_okay=False,
                                dir_okay=True),
              default=os.path.join(os.path.curdir, 'hardcopy.d')
              )
@click.argument('input', type=click.File('rb'), required=True)
@click.pass_context
def backup(ctx, barcode, to, segment_size, build_dir, input):
 
    if os.path.exists(build_dir):
        ## Incompatible with taking click input from stdin
        #click.confirm('Backup directory exists. Overwrite?', abort=True)
        #secure_rm_rf(os.path.join(os.path.curdir,build_dir))
        logging.error(
            'Directory %s already exists.' % (build_dir)
        )
        exit(1)

    hc = HardcopyBackup(input,
                        barcode,
                        to,
                        segment_size,
                        build_dir)

    hc.mk_build_dir()
    
    #for barcode in hc.generate_barcodes():
    #    logging.info(barcode['hash'].hexdigest())
    #    logging.info(barcode['barcode_filename'])

    hc.jinja2_render()

    return

def secure_rm_rf(dir):
    for (dirpath, dirnames, filenames) in os.walk(dir):
        for filename in filenames:
            os.remove(os.path.join(dirpath,filename))
    os.rmdir(dir)

if __name__ == '__main__':
    cli()
