#!/usr/bin/python3

from pyx import *

def main ():
    key = '6A9FB506'
    c = canvas.canvas()
    ef = epsfile.epsfile(0, 0, "%s.key.asca.eps" % (key))
    c.insert(ef)
    c.text(ef.bbox().left(), ef.bbox().bottom(), "Hello, wurld.", [])
    c.writeEPSfile("output")

if __name__ == '__main__':
        main()
