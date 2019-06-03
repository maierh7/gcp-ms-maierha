
from datetime import datetime as dt
from datetime import timezone as tz

class UTC:
    utc = None
    
    def __init__ (self):
        self.utc = dt.now (tz.utc)
        
    def date (self):
        return self.utc.date ()
    
    def time (self):
        ti = self.utc
        return ti.replace (microsecond=0).time ()
