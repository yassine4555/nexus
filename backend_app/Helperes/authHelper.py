from supaBase.supaBase import dataBaseAuth



class authHelper : 
    def __init__(self,database : dataBaseAuth):
        self.authenticater=database
    
    def CreateUser(self,Email,password) -> bool:
        try:
            result = self.authenticater.createUser(Email,password)
            return result is not None
        except Exception as e:
            print(f"Auth creation error: {e}")
            return False
        
    
    def login (self,Email,password) -> bool:
        try:
            result = self.authenticater.login(Email,password)
            return result is not None
        except Exception as e:
            print(f"Auth login error: {e}")
            return False
