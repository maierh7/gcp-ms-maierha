
import re
import sys
import iso8601
import time
import string
import random

from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.cloud import storage

# import json
from pprint import pprint

from datetime import timedelta
from datetime import timezone
from datetime import datetime

def get_rand_postfix ():
    postfix = ''.join (random.choice(string.ascii_lowercase) for _ in range (4))
    return postfix


class SQLAdm:
    sqladm   = None
    storage  = None
    project  = None
    backend  = None
    version  = None
    instance = None
    
    backups  = dict () # id [st, wt, et, status, type]
    blst     = dict () # date [dt1, dt2, ...]
    bids     = dict () # dt [id1, id2, ...]

    dbs      = list () # databases list
    
    now_dt   = None
    
    opt_last = 50      # check for the last backup minutes back
    opt_keep_per_day = 10
    opt_keep_days    = 14
    
    def __init__ (self, project, instance, credentials, all_backups=False):
        """Constructor."""
        ndt = datetime.now (timezone.utc)
        self.now_dt = ndt.replace (microsecond=0)
        self.project = project
        self.instance = instance
        self.sqladm = discovery.build ("sqladmin", "v1beta4", credentials=credentials, cache_discovery=False)
        self.get_backups (all_backups)

    def get_backups (self, all_backups=False):
        """Gets all the on-demand backups if all is false. If all
        is true it gets also the automated backups. The first one is
        used for On-demand backups the second one for recovery.
"""
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
                    if all_backups is False and ty == 'AUTOMATED':
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

    def get_backups_all (self, full=False):
        """List all the backups - On-demand and automated backups.
"""
        req = self.sqladm.backupRuns().list (project=self.project, instance=self.instance)
        while req:

            try:
                res = req.execute ()
            except HttpError as err:
                if err.resp.status in [429]:
                    # No backups available
                    return
            
            for bkp in res['items']:
                if full == True:
                    print (bkp)
                else:
                    tid   = bkp['id']
                    start = ""
                    if 'startTime' not in bkp:
                        start = bkp['enqueuedTime']
                    else:
                        start  = bkp['startTime']
                    status = bkp['status']
                    ttyp   = bkp['type']
                    print ("%s %s %s %s" % (tid, start, ttyp, status))
                    
            req = self.sqladm.backupRuns().list_next (previous_request=req, previous_response=res)
            
    def print_backups (self, all_backups = False):
        """This prints the backup dictionary.
"""
        if all_backups is True:
            self.get_backups (all)
        for i in self.backups:
            print (i, self.backups [i])

    def print_blst (self):
        """Prints the backup list in a human readable manner:
date9 : time1 time2 ...
date8 : time1 time2 ...
date7 : time1
...
"""
        print ("Now:")
        print (self.now_dt.date (), self.now_dt.time())
        print ("Backup-List")
        for i in sorted (self.blst, reverse=True):
            print (i, end=": ")
            for j in self.blst[i]:
                print (j.replace (microsecond=0).time (), end= " ")
            print ()
            
    def print_bids (self):
        """Prints the backup ids dictionary with the assigned date-times.
"""
        print ("IDs (%d):" % (len(self.bids)))
        for i in sorted (self.bids, reverse=True):
            bck = self.backups[self.bids[i]]
            ttyp = bck[4]
            stat = bck[3]
            print (self.bids[i], i, ttyp, stat)

    def print_version (self):
        print (self.version, self.backend)
        
    def get_db_type (self):
        req = self.sqladm.instances().list (project=self.project)
        
        try:
            res = req.execute ()
        except HttpError as err:
            print (err.resp.status)
            if err.resp.status in [429]:
                self.version = "POSTGRES_9_6"
                self.backend = "SECOND_GEN"
                return
        except:
            print (sys.exc_info()[0])
            return

        if len (res) == 0:
            print ("Error: no instnace", file=sys.stderr)
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
        """Execute the on-demand backup request.
"""
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
        """Delete backup request.
"""
        res = self.sqladm.backupRuns ().delete (project=self.project, instance=self.instance, id=bid).execute ()
        if len (res):
            print (res['status'], res['user'])

    def delete_old_backups (self):
        """Delete old on-demand backups.
"""
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
        """Get the databases into the self.dbs dictionary.
"""
        req = self.sqladm.databases().list (project=self.project, instance=self.instance)
        res = req.execute ()
        for i in res['items']:
            self.dbs.append (i['name'])
    
    def file_exists (self, bucket, filename):
        """Test if an filename exists in an storage buckett.
"""
        buck = self.storage.get_bucket (bucket)
        blobs = self.storage.list_blobs (buck)
        for i in blobs:
            if i.name == filename:
                return True
        return False
    
    def export (self):
        """Export the instance to the storage bucket. The storage bucket
        name should have the following format: project - instance_name
"""
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

    def restore_backup_req (self, bid, trg_project, trg_instance):
        """Backup request
"""
        restore = {
            "restoreBackupContext" : {
                "kind" : "sql#restoreBackupContext",
                "backupRunId" : bid,
                "project" : self.project,
                "instanceId" : self.instance,
                }
            }
        req = self.sqladm.instances ().restoreBackup (project=trg_project, instance=trg_instance, body = restore)
        res = req.execute ()
        print ("Restroe request pending")

    def restore_backup (self, bid=None, project=None, instance=None):
        """Restore the instance with the given backup run Id. If Id is
        none then use the last backup run.
"""
        trg_project  = self.project
        trg_instance = self.instance
        
        if project is not None:
            trg_project = project
        if instance is not None:
            trg_instance = instance
            
        restore_id = bid
        self.get_backups (all_backups=True)
        for i in sorted (self.bids, reverse=True):
            tid  = self.bids[i]
            if restore_id is None:
                restore_id = tid
            bck  = self.backups[self.bids[i]]
            st   = bck[0]
            stat = bck[3]
            if tid == restore_id and stat == 'SUCCESSFUL':
                print (tid, st, stat)
                self.restore_backup_req (tid, trg_project, trg_instance)
                return
        print ("Warning: Successful Backup for %d not found")

    def get_instance (self):
        req = self.sqladm.instances ().get(project=self.project, instance=self.instance)
        res = req.execute ()
        return res
    
    def create_instance (self, trg_project):
        sbod = self.get_instance ()
        name = self.instance + "-" + get_rand_postfix ()
        body = {
            "name" : name,
            "backendType"     : sbod['backendType'],
            "databaseVersion" : sbod['databaseVersion'],
            "region"          : sbod['region'],
            "settings": {
                "tier": sbod ['settings'] ['tier'],
                "locationPreference" : {
                    "zone" : sbod['settings']['locationPreference']['zone']
                    },
                },
            }
        print (trg_project)
        pprint (body)
        req = self.sqladm.instances().insert (project=trg_project, body=body)
        res = req.execute ()
        pprint (res)
