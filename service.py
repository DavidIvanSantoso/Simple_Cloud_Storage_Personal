from unicodedata import name
from nameko.rpc import rpc

import dependencies.database as database

class CloudService:
    name='cloud_service'
    database=database.DatabaseProvider()

    @rpc
    def register(self,username,password):
        reg=self.database.register(username,password)
        return reg
    
    @rpc
    def login(self,username,password):
        log=self.database.login(username,password)
        return log

    @rpc
    def logout(self):
        log=self.database.logout()
        return log