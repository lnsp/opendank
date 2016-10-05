from sources import *
from diashow import ImageDiashow

dia = ImageDiashow()
dia.add_source(RedditSource())
dia.add_source(SysadminotaurSource())
dia.add_source(XkcdSource())
dia.start()
