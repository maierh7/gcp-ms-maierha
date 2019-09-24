
from oauth2client.client import GoogleCredentials as client    
from googleapiclient import discovery
from googleapiclient.errors import HttpError

class SQL:
    sql = None
    proj = None
    items = None
    
    def __init__ (self, proj, credentials):
        self.proj = proj
        self.sql = discovery.build ("sqladmin", "v1beta4", credentials=credentials)
        self.items = list ()
        self.get_items ()

    def get_items (self):

        req = self.sql.instances().list (project=self.proj)
        while req:
            res = req.execute ()
            for i in res['items']:
                self.items.append (i)
            req = self.sql.instances().list_next (previous_request=req, previous_response=res)

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
    
