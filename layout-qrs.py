#!/usr/bin/python3

from pyx import *

def main ():

    c = canvas.canvas()
    
    key = '6A9FB506'
    c1 = canvas.canvas()
    ef = epsfile.epsfile(0, 0, "%s.key.asca.eps" % (key))
    c1.insert(ef)
    c1.text(ef.bbox().left(), ef.bbox().bottom(), "Hello, wurld.", [])

    c.insert(c1)
        
    pg = document.page(mc, paperformat=document.paperformat.Letter, centered=1, )
    doc = document.document([pg])
    doc.writePSfile('output')
    return

if __name__ == '__main__':
    main()
