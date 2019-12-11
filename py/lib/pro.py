
import os

from googleapiclient import discovery
from googleapiclient.errors import HttpError

class Project:

    service = None

    plst = dict () # name [id]
    
    def __init__ (self, credentials):
        self.service = discovery.build ('cloudresourcemanager', 'v1', credentials=credentials)
        self.get_all ()
        
    def get_all (self):
        req = self.service.projects().list()

        while req:
            res = req.execute ()
            for pro in res.get ('projects', []):
                self.plst [pro['name']] = pro['projectId']
            req = self.service.projects().list_next(previous_request=req, previous_response=res)

    def get_id (self, name):
        return (self.plst[name])

    def get_name (self, id):
        for na, i in self.plst.items ():
            if i == id:
                return na
        return None
