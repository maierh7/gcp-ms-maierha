
import re
import sys

from pprint import pprint
from enum import Enum

from oauth2client.client import GoogleCredentials as client    
from googleapiclient import discovery
from googleapiclient.errors import HttpError

class SQL_Status (Enum):
    LIST  = 0
    EMPTY = 1
    PERM  = 2

def get_gb (sbytes):
    val = int (sbytes)
    if val == 0:
        return 0
    return val / (1024 * 1024 * 1024)

def get_cpu_ram (tier):
    tiers = {
        "db-f1-micro"      :    0.600,
        "db-g1-small"      :    1.700,
        "db-n1-standard-1" :    3.750,
        "db-n1-standard-2" :    7.500,
        "db-n1-standard-4" :   15.000,
        "db-n1-standard-8" :   30.000,
        "db-n1-standard-16":  60.000,
        "db-n1-standard-32": 120.000,
        "db-n1-standard-64": 240.000,
        "db-n1-highmem-2"  :   13.000,
        "db-n1-highmem-4"  :   26.000,
        "db-n1-highmem-8"  :   52.000,
        "db-n1-highmem-16" :  104.000,
        "db-n1-highmem-32" :  208.000,
        "db-n1-highmem-64" :  416.000,
    }
    cpu = 0
    ram = 0
    if tier in tiers:
        ram = tiers [tier]
    m1 = re.match ("^db-n1-(?:standard|highmem)-([0-9]+)", tier)
    if m1:
        cpu = m1.group (1)
    m2 = re.match ("^db-custom-([0-9]+)-([0-9]+)$", tier)
    if m2:
        cpu = m2.group (1)
        ram = m2.group (2)
    return (float (cpu), float (ram) / 1024)

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
            # try:
            res = req.execute ()
            # except HttpError as err:
            #     if err.resp.status in [403]:
            #         return SQL_Status.PERM
            #     print (self.proj)
            #     print ("HTTP-Error (Inst-Count): ", err.resp.status)
            #     sys.exit ()
                
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

    def get_dr (self):
        res = dict ()
        for i in self.items:
            inst = i['name']
            avai = 'ZONAL'
            if 'availabilityType' in i['settings']:
                avai = i['settings']['availabilityType']
            auto = i['settings']['backupConfiguration']['enabled']
            binl = False
            if 'binaryLogEnabled' in i['settings']['backupConfiguration']:
                binl = i['settings']['backupConfiguration']['binaryLogEnabled']
            res [inst] = (avai, auto, binl)
        return res

    def get_size (self):
        res = dict ()
        for i in self.items:
            inst = i['name']
            dtyp = i['databaseVersion']
            size = i['settings']['dataDiskSizeGb']
            htyp = i['settings']['dataDiskType']
            res [inst] = [dtyp, size, htyp]
        return res
    
    def get_backup_count (self, inst):
        ind = 0
        req = self.sql.backupRuns().list (project=self.proj, instance=inst)

        while req:

            try:
                res = req.execute ()
            except HttpError as err:
                if err.resp.status in [429]:
                    # No backups available
                    return -1

            if "items" not in res:
                continue

            for i in res["items"]:
                ind = ind + 1
            req = self.sql.backupRuns().list_next (previous_request=req, previous_response=res)
        return ind

    def get_all_tiers (self):
        res = self.sql.tiers().list(project = self.proj).execute ()
        for i in res ['items']:
            print ("%7.3f %10.0f %s" % (get_gb (i['RAM']), get_gb(i['DiskQuota']),i['tier']))
