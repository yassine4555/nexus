import uuid
from supaBase.supaBase import dataBaseAuth
from modeles.user import User
from testStore.userJson import JsonUserStore
from Helperes.passwordHelper import passwordHelper
from modeles.role import ROLE


class userHelper :

    @staticmethod
    def getUserByEmail(email: str) -> User:
        AllUseres = JsonUserStore("./userJson.json").get_all_users()
        for user in AllUseres:
            if user.Email == email:
                return user
        return None

    @staticmethod
    def CreateUser(Email, FirstName, LastName,  DateOfBirth,  Address , password):
        try:
            Jstore = JsonUserStore("./userJson.json")
            ID = str(uuid.uuid4())
            newUser = User(Email, FirstName, LastName, ID, DateOfBirth, Address, EmployeesList=[])
            Jstore.add_user(newUser)
            passwordHelper.assignPasswordToUser(newUser.ID, password)
            return True, newUser  # ✅ Return tuple
        except Exception as e:
            print(f"Create user error: {e}")
            return False, None  # ✅ Return tuple

    @staticmethod
    def getAllUsers(type=None):
        users = JsonUserStore("./userJson.json").get_all_users()
        if type is not None:
            users = [user for user in users if user.Role == type]
        return users

    @staticmethod
    def removeEmployee(user, emp):
        if emp in user.EmployeesList:
            user.EmployeesList.remove(emp)

    @staticmethod
    def assignCodeToManager(manager: User, code):
        codes = JsonUserStore("./codes.json")
        codes.codeToMangaer(manager, code)
    
    @staticmethod
    def getManagerFromCode(code):
        data = JsonUserStore("./codes.json").get_all_code()
        for item in data:
            for user_id, stored_code in item.items():
                if stored_code == code:
                    return user_id
        return None
    
    @staticmethod
    def addemployerTomanager(manager: User, user: User):
        try:
            # ✅ Load the JSON store
            Jstore = JsonUserStore("./userJson.json")
            
            # ✅ Append User ID instead of entire User object
            if user.Email not in manager.EmployeesList:
                manager.EmployeesList.append(user.Email)
            
            # ✅ Update the manager using the existing update_user method
            # Read current data
            with open("./userJson.json", 'r') as f:
                import json
                data = json.load(f)
            
            # Update the manager's data
            if manager.ID in data:
                data[manager.ID]['EmployeesList'] = manager.EmployeesList
            
            # Write back to file
            with open("./userJson.json", 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error adding employer to manager: {e}")
            import traceback
            traceback.print_exc()
            return False
