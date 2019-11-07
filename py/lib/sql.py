
import sys
from enum import Enum

from oauth2client.client import GoogleCredentials as client    
from googleapiclient import discovery
from googleapiclient.errors import HttpError

class SQL_Status (Enum):
    LIST  = 0
    EMPTY = 1
    PERM  = 2

class SQL:
    
    sql = None
    proj = None
    items = None

    status = SQL_Status.LIST
    
    def __init__ (self, proj, credentials):
        self.proj = proj
        self.sql = discovery.build ("sqladmin", "v1beta4", credentials=credentials)
        self.items = list ()
        self.status = self.get_items ()

    def get_items (self):

        req = self.sql.instances().list (project=self.proj)
        while req:
            try:
                res = req.execute ()
            except HttpError as err:
                if err.resp.status in [403]:
                    return SQL_Status.PERM
                print (self.proj)
                print ("HTTP-Error: ", err.resp.status)
                sys.exit ()
                
            if 'items' not in res:
                # No SQL instances
                return SQL_Status.EMPTY
            
            for i in res['items']:
                self.items.append (i)
            req = self.sql.instances().list_next (previous_request=req, previous_response=res)
            return SQL_Status.LIST

    def list (self):
        lst = list ()
        for i in self.items:
            inst = i['name']
            lst.append (inst)
        return lst

    def get_sa (self):
        res = dict ()
        for i in self.items:
            inst = i['name']
            sama = i['serviceAccountEmailAddress']
            res [inst] = sama
        return res
    
    def get_backup_count (self, inst, cred):
        adm = discovery.build ("sqladmin", "v1beta4", credentials=cred)

        ind = 0
        req = adm.backupRuns().list (project=self.proj, instance=inst)
        while req:
            res = req.execute ()

            if "items" not in res:
                continue

            for i in res["items"]:
                ind = ind + 1
            req = adm.backupRuns().list_next (previous_request=req, previous_response=res)
        return ind

