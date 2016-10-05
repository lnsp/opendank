from redditsource import RedditSource
from opendank import ImageDiashow
from comicsources import *

dia = ImageDiashow()
dia.add_source(RedditSource())
dia.add_source(SysadminotaurSource())
dia.add_source(XkcdSource())
dia.start()