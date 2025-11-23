import os
from supabase import create_client, Client ,ClientOptions
import httpx

class dataBaseAuth :
    def __init__(self, url,key):
    
        timeout = httpx.Timeout(100.0, connect=100.0)  # 30s timeout, 10s connect
        http_client = httpx.Client(timeout=timeout)
        options = ClientOptions({
            'auth': {'http_client': http_client}
        })
        self.supabase: Client = create_client(url, key,options)
    
    def createUser(self, email,password):
        return self.supabase.auth.sign_up(
    {
        "email": f"{email}",
        "password": f"{password}",
    })
        
    

    def login(self,email,password):
        return self.supabase.auth.sign_in_with_password(
        {
            "email": f"{email}",
            "password": f"{password}",
        }
)

        
    
