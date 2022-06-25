import json
from tkinter.ttk import Separator
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from dependencies.session import SessionProvider
import os

class GatewayService:
    name='gateway'
    database=RpcProxy('cloud_service')
    session_provider = SessionProvider()

    @http('POST','/register')
    def register(self,request):
        username=""
        password=""
        data = format(request.get_data(as_text=True))
        array = data.split("&")
        for file in array:
            cnt=file.split("=")
            if cnt[0]=="username":
                username=cnt[1]
            if cnt[0]=="password":
                password=cnt[1]
        data_regis=self.database.register(username,password)
        return json.dups(data_regis)
    
    @http('GET', '/login')
    def login(self, request):
        username = "" 
        password = "" 
        data=format(request.get_data(as_text=True))
        array=data.split("&")
        for file in array:
            cnt     = file.split("=")
            if cnt[0] == "username":
                username = cnt[1]
            if cnt[0] == "password":
                password = cnt[1]
        flags = self.database.login(username, password)
        
        if(flags == 1):
            user_data = {
                'username': username,
                'password': password
            }
            session_id = self.session_provider.set_session(user_data)
            response = Response(str(user_data))
            response.set_cookie('SESSID', session_id)
            return response
        
        
    @http('POST','/logout')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            confirm = self.session_provider.delete_session(cookies['SESSID'])
            if (confirm):
                response = Response('Logout Successful')
                response.delete_cookie('SESSID')
            else:
                response = Response("Logout Failed")
            return response
    
    @http("GET", "/<string:namafile>")
    def download_file(self, request,namafile):
        file_name, file_extension = os.path.splitext(namafile)
        if namafile is None:
            return json.dumps({"Can't find file": False})
        else:
            return Response(open(f"saved_{namafile}", "rb").read(), mimetype="application/{file_extension}")
    

