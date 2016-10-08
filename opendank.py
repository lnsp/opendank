#!/usr/bin/python2
import diashow
import sys
import sources

def main():
    if len(sys.argv) < 2:
        print 'Missing configuration argument'
        return

    dia = diashow.Diashow()
    with file(sys.argv[1]) as f:
        for line in f:
            dia.add_source(sources.CustomSource(line))
    dia.start()

if __name__ == "__main__":
    main()
