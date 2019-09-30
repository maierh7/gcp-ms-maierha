
import re
import sys
import iso8601
import time

from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.cloud import storage

# import json
# from pprint import pprint

from datetime import timedelta
from datetime import timezone
from datetime import datetime

class SQLAdm:
    sqladm   = None
    storage  = None
    project  = None
    backend  = None
    version  = None
    instance = None
    
    backups  = dict () # id [st, et, status]
    blst     = dict () # date [dt1, dt2, ...]
    bids     = dict () # dt [id1, id2, ...]

    dbs      = list ()
    
    now_dt   = None
    
    opt_last = 50      # check for the last backup minutes back
    opt_keep_per_day = 10
    opt_keep_days    = 14
    
    def __init__ (self, project, instance, credentials):
        ndt = datetime.now (timezone.utc)
        self.now_dt = ndt.replace (microsecond=0)
        self.project = project
        self.instance = instance
        self.sqladm = discovery.build ("sqladmin", "v1beta4", credentials=credentials, cache_discovery=False)
        self.get_backups ()

    def get_backups (self):
        self.get_db_type ()

        self.backups.clear ()
        self.blst.clear ()
        self.bids.clear ()
        
        req = self.sqladm.backupRuns().list (project=self.project, instance=self.instance)

        while req is not None:

            res = None
            try:
                res = req.execute ()
            except HttpError as err:
                if err.resp.status in [429]:
                    # No backups available
                    return

            if res is None:
                print ("Error: wrong project (%s) or instance (%s)" %(self.project, self.instance),
                       file=sys.stderr)
                sys.exit (1)
                       
            if 'items' not in res:
                continue

            for bkp in res['items']:
                et = None
                if 'endTime' in bkp:
                    et = bkp['endTime']
                    st = bkp['startTime']
                    ty = bkp['type']
                    if ty == 'AUTOMATED':
                        continue
                    self.backups [bkp['id']] = [st, bkp['windowStartTime'], et, bkp['status'], bkp['type']]
            req = self.sqladm.backupRuns().list_next (previous_request=req, previous_response=res)
            
        # Build blst and bids
        for i in self.backups:
            dt = iso8601.parse_date (self.backups[i][0])
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
            bck = self.backups[self.bids[i]]
            type = bck[4]
            print (self.bids[i], i, type)

    def print_version (self):
        print (self.version, self.backend)
        
    def get_db_type (self):
        req = self.sqladm.instances().list (project=self.project)
        
        try:
            res = req.execute ()
        except HttpError as err:
            if err.resp.status in [429]:
                self.version = "POSTGRES_9_6"
                self.backend = "SECOND_GEN"
                return
            
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
        for i in sorted (self.blst, reverse=True):
            for j in self.blst[i]:
                if j + timedelta (days=self.opt_keep_days) < self.now_dt:
                    print ("Delete Backup:" + str(j))
                    self.delete_backup (self.bids[j])

    def get_databases (self):
        req = self.sqladm.databases().list (project=self.project, instance=self.instance)
        res = req.execute ()
        for i in res['items']:
            self.dbs.append (i['name'])
    
    def file_exists (self, bucket, filename):
        buck = self.storage.get_bucket (bucket)
        blobs = self.storage.list_blobs (buck)
        for i in blobs:
            if i.name == filename:
                return True
        return False
    
    def export (self):
        self.storage = storage.Client ()
        print (self.project, self.instance, self.version)
        body = {
            "exportContext": {
                "kind": "sql#exportContext",
                "fileType": "SQL",
                "uri": "",
                "databases": [],
            }
        }
        if self.version == "MYSQL_5_7":
            bu = self.project + "-" + self.instance 
            fn = str(self.now_dt.date ())
            body["exportContext"]["uri"] = "gs://" + bu + "/" + fn 
            print (body["exportContext"]["uri"])
            req = self.sqladm.instances().export (project=self.project, instance=self.instance, body=body)
            req.execute ()
        else:
            self.get_databases ()
            for i in self.dbs:
                bu = self.project + "-" + self.instance 
                fn = str(self.now_dt.date ()) + "/" + i
                if self.file_exists (bu,fn) == True:
                    print (bu,fn, "file exists")
                    continue
                body["exportContext"]["uri"] = "gs://" + bu + "/" + fn 
                # Only One Database just now possible
                body["exportContext"]["databases"].clear ()
                body["exportContext"]["databases"].append (i)
                print (body["exportContext"]["uri"])
                req = self.sqladm.instances().export (project=self.project, instance=self.instance, body=body)
                req.execute ()
            
                while self.file_exists (bu, fn) is False:
                    time.sleep (15)
 
