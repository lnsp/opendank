#!/usr/bin/python2
import diashow, sources

dia = diashow.Diashow()
dia.add_source(sources.Reddit)
dia.add_source(sources.Sysadminotaur)
dia.add_source(sources.Xkcd)
dia.start()
