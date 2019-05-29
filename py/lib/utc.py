
from datetime import datetime as dt
from datetime import date     as da
from datetime import time     as ti

class UTC:
    utc = None
    
    def __init__ (self):
        now = dt.now ().astimezone()
        self.utc = now - now.utcoffset ()

    def date (self):
        return self.utc.date ()
    
    def time (self):
        ti = self.utc
        return ti.replace (microsecond=0).time ()
