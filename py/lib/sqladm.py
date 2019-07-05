
import re
import sys
from googleapiclient import discovery

# import json
# from pprint import pprint

from datetime import timedelta
from datetime import timezone
from datetime import datetime

class SQLAdm:
    sqladm   = None
    project  = None
    backend  = None
    version  = None
    instance = None
    backups  = dict () # id [st, et, status]

    blst     = dict () # date [dt1, dt2, ...]
    bids     = dict () # dt [id1, id2, ...]

    now_dt   = None
    
    opt_last = 45      # check for the last backup minutes back
    opt_keep_per_day = 10
    opt_keep_days    = 14
    
    def __init__ (self, project, instance, credentials):
        ndt = datetime.now (timezone.utc)
        self.now_dt = ndt.replace (microsecond=0)
        self.project = project
        self.instance = instance
        self.sqladm = discovery.build ("sqladmin", "v1beta4", credentials=credentials)
        self.get_backups ()

    def get_backups (self):
        self.get_db_type ()
        
        req = self.sqladm.backupRuns().list (project=self.project, instance=self.instance)

        while req is not None:
            res = req.execute ()

            for bkp in res['items']:
                et = None
                if 'endTime' in bkp:
                    et = bkp['endTime']
                    self.backups [bkp['id']] = [bkp['startTime'], et, bkp['status']]
            req = self.sqladm.backupRuns().list_next (previous_request=req, previous_response=res)
            
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
        print ("IDs (%d):" % (len(self.bids)))
        for i in sorted (self.bids, reverse=True):
            print (self.bids[i], i)

    def print_version (self):
        print (self.version, self.backend)
        
    def get_db_type (self):
        res = self.sqladm.instances().list (project=self.project).execute ()
        for i in res['items']:
            name = None
            back = None
            vers = None
            for j in i:
                if j == "backendType":
                    back = i['backendType']
                if j == "databaseVersion":
                    vers = i['databaseVersion']
                if j == "name":
                    name = i['name']
            if name == self.instance:
                self.version = vers
                self.backend = back

    def do_backup (self):
        m = re.match ("^POSTGRES", self.version)
        if m is None:
            print ("Error: extented backup is only necessary for PostgreSQL", file=sys.stderr)
            return
        backup = False
        if self.now_dt.date() not in self.blst:
            backup = True
        else:
            cur_last = self.blst[self.now_dt.date()][0]
            if self.now_dt > cur_last + timedelta (minutes=self.opt_last):
                backup = True
            
        print (self.now_dt, backup)
        if backup == True:
            body = {}
            # Ignore result. Job is always pending.
            self.sqladm.backupRuns ().insert (project=self.project, instance=self.instance, body=body).execute ()
            
    def delete_backup (self, bid):
        res = self.sqladm.backupRuns ().delete (project=self.project, instance=self.instance, id=bid).execute ()
        if len (res):
            print (res['status'], res['user'])

    def delete_old_backups (self):
        cnt = 0
        delete = False
        for i in sorted (self.blst, reverse=True):
            start_idx = 0
            if i < self.now_dt.date ():
                start_idx = 1
            for j in self.blst[i][start_idx:]:
                cnt += 1
                print ("%2d %s %s %1d %s" % (cnt, i, j, start_idx, delete))
                # keep at least one backup for days less than current
                if delete == True:
                    self.delete_backup (self.bids[j])
                if cnt >= self.opt_keep_per_day:
                    delete = True
        for i in sorted (self.blst, reverse=True)[self.opt_keep_days:]:
            print (i)
            for j in self.blst[i]:
                self.delete_backup (self.bids[j])
