import requests
import uuid
from modeles.user import User
from modeles.role import ROLE
from Helperes.passwordHelper import passwordHelper

# Configuration for Nexus Data Service
NEXUS_API_URL = "http://127.0.0.1:5001"
INTERNAL_API_KEY = "nexus-internal-secret-key-123"
HEADERS = {"X-Internal-Key": INTERNAL_API_KEY}

class userHelper:

    @staticmethod
    def getUserByEmail(email: str) -> User:
        try:
            # Fetch all users and filter (inefficient but matches previous logic)
            # Better: Fetch specific user if API supports it
            response = requests.get(f"{NEXUS_API_URL}/users/", headers=HEADERS)
            if response.status_code == 200:
                users_data = response.json()['data']
                for u_data in users_data:
                    if u_data.get('email') == email:
                        return User.from_dict(userHelper._map_nexus_to_backend(u_data))
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    @staticmethod
    def CreateUser(Email, FirstName, LastName, DateOfBirth, Address, password):
        try:
            payload = {
                "email": Email,
                "first_name": FirstName,
                "last_name": LastName,
                "date_of_birth": DateOfBirth,
                "address": Address,
                "password": password,
                "role": "employee" # Default role
            }
            
            response = requests.post(f"{NEXUS_API_URL}/users/", json=payload, headers=HEADERS)
            
            if response.status_code == 201:
                user_data = response.json()['data']
                new_user = User.from_dict(userHelper._map_nexus_to_backend(user_data))
                return True, new_user
            else:
                print(f"API Error: {response.text}")
                return False, None
        except Exception as e:
            print(f"Create user error: {e}")
            return False, None

    @staticmethod
    def getAllUsers(type=None):
        try:
            response = requests.get(f"{NEXUS_API_URL}/users/", headers=HEADERS)
            if response.status_code == 200:
                users_data = response.json()['data']
                users = [User.from_dict(userHelper._map_nexus_to_backend(u)) for u in users_data]
                
                if type is not None:
                    # Filter by role (Nexus uses lowercase strings, Backend uses Enum or string?)
                    # Assuming Backend ROLE enum values match or we need to map
                    target_role = type.value if hasattr(type, 'value') else type
                    users = [u for u in users if u.Role == target_role]
                return users
            return []
        except Exception as e:
            print(f"Get all users error: {e}")
            return []

    @staticmethod
    def removeEmployee(user, emp):
        # This logic seems to be about removing a relationship
        # Nexus handles this via manager_id update
        pass

    @staticmethod
    def assignCodeToManager(manager: User, code):
        try:
            payload = {
                "manager_id": manager.ID,
                "code": code,
                "max_uses": 1 # Default to 1 use?
            }
            requests.post(f"{NEXUS_API_URL}/invites/", json=payload, headers=HEADERS)
        except Exception as e:
            print(f"Assign code error: {e}")
    
    @staticmethod
    def getManagerFromCode(code):
        try:
            response = requests.get(f"{NEXUS_API_URL}/invites/{code}", headers=HEADERS)
            if response.status_code == 200:
                data = response.json()['data']
                if data['is_active']:
                    # Return manager's email or ID? 
                    # Original code returned user_id (which was email in some contexts or ID?)
                    # Original: return user_id from codes.json
                    # Nexus returns manager_id (int). Backend User ID is UUID?
                    # Wait, Nexus User ID is Integer. Backend User ID is UUID (in CreateUser).
                    # We might have a mismatch here. 
                    # Nexus User ID is int. Backend expects what?
                    # Let's return the manager's email if possible, or we need to fetch the manager.
                    
                    # Fetch manager details
                    manager_id = data['manager_id']
                    manager_res = requests.get(f"{NEXUS_API_URL}/users/{manager_id}", headers=HEADERS)
                    if manager_res.status_code == 200:
                        return manager_res.json()['data']['email']
            return None
        except Exception as e:
            print(f"Get manager from code error: {e}")
            return None
    
    @staticmethod
    def addemployerTomanager(manager: User, user: User):
        try:
            # Update the user's manager_id in Nexus
            # We need the user's Nexus ID (int), but we might only have their email or Backend UUID.
            # We need to look up the user by email first to get their Nexus ID.
            
            # 1. Get User's Nexus ID
            target_user = userHelper.getUserByEmail(user.Email)
            if not target_user: return False
            
            # 2. Get Manager's Nexus ID
            target_manager = userHelper.getUserByEmail(manager.Email)
            if not target_manager: return False
            
            # Nexus ID is stored in ID field? 
            # In _map_nexus_to_backend, we map Nexus ID (int) to User.ID?
            # Original Backend User used UUID. Nexus uses Int.
            # We should probably use Nexus ID as the ID in Backend User object now.
            
            payload = {"manager_id": target_manager.ID}
            requests.put(f"{NEXUS_API_URL}/users/{target_user.ID}", json=payload, headers=HEADERS)
            return True
        except Exception as e:
            print(f"Add employer to manager error: {e}")
            return False

    @staticmethod
    def _map_nexus_to_backend(nexus_data):
        """Helper to map Nexus API response to Backend User dict format"""
        # Nexus: id (int), email, first_name, last_name, role, department, etc.
        # Backend User: Email, FirstName, LastName, ID, DateOfBirth, Address, EmployeesList, Role, Department
        
        return {
            "Email": nexus_data.get('email'),
            "FirstName": nexus_data.get('first_name'),
            "LastName": nexus_data.get('last_name'),
            "ID": nexus_data.get('id'), # Using Nexus Int ID
            "DateOfBirth": nexus_data.get('date_of_birth'),
            "Address": nexus_data.get('address'),
            "Role": nexus_data.get('role'), # String match?
            "Department": nexus_data.get('department'),
            "EmployeesList": [] # Nexus doesn't return this list directly in user object usually
        }
