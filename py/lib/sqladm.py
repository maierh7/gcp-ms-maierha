
import json
from pprint import pprint
from googleapiclient import discovery

from datetime import date
from datetime import time
from datetime import timedelta
from datetime import timezone
from datetime import datetime

class SQLAdm:
    sqladm   = None
    project  = None
    instance = None
    backups  = dict () # id [st, et, status]

    blst     = dict () # date [dt1, dt2, ...]
    bids     = dict () # dt [id1, id2, ...]

    now_dt   = None
    
    def __init__ (self, project, instance, credentials):
        ndt = datetime.now (timezone.utc)
        self.now_dt = ndt.replace (microsecond=0)
        self.project = project
        self.instance = instance
        self.sqladm = discovery.build ("sqladmin", "v1beta4", credentials=credentials)

    def get_backups (self):
        res = self.sqladm.backupRuns ().list (project=self.project, instance=self.instance).execute ()
        for bkp in res['items']:
            et = None
            if 'endTime' in bkp:
                et = bkp['endTime']
            self.backups [bkp['id']] = [bkp['startTime'], et, bkp['status']]
        # Build blst and bids
        for i in self.backups:
            dt = datetime.strptime (self.backups[i][0], "%Y-%m-%dT%H:%M:%S.%f%z")
            da = dt.date ()
            #print (da, dt)
            if da not in self.blst:
                self.blst[da] = list ()
            self.blst[da].append (dt)
            self.bids[dt] = i
            
    def print_backups (self):
        for i in self.backups:
            print (i, self.backups [i])

    def print_blst (self):
        print ("Now:")
        print (self.now_dt.date (), self.now_dt.time())
        print ("Backup-List")
        for i in sorted (self.blst, reverse=True):
            print (i, end=": ")
            for j in self.blst[i]:
                print (j.replace (microsecond=0).time (), end= " ")
            print ()
            
    def print_bids (self):
        print ("IDs:")
        for i in sorted (self.bids, reverse=True):
            print (self.bids[i], i)
