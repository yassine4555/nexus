import json
from typing import Optional, List
from modeles.user import User
from modeles.department import Department
from modeles.role import ROLE


class JsonUserStore:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        try:
            with open(self.filepath, 'r') as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.filepath, 'w') as f:
                json.dump({}, f)

    def add_user(self, user: User):
        """Add or update a user in the store"""
        data = self._read()
        data[user.ID] = self._user_to_dict(user)
        self._write(data)

    def get_user(self, userid: str) -> Optional[User]:
        """Retrieve a user by ID"""
        data = self._read()
        user_data = data.get(userid)
        if user_data:
            return self._dict_to_user(user_data)
        return None

    def get_all_users(self) -> List[User]:
        """Retrieve all users"""
        data = self._read()
        return [self._dict_to_user(user_data) for user_data in data.values()]

    def delete_user(self, userid: str) -> bool:
        """Delete a user by ID. Returns True if deleted, False if not found"""
        data = self._read()
        if userid in data:
            del data[userid]
            self._write(data)
            return True
        return False

    def user_exists(self, userid: str) -> bool:
        """Check if a user exists"""
        data = self._read()
        return userid in data

    def _user_to_dict(self, user: User) -> dict:
        """Convert User object to dictionary"""
        return {
            'ID': user.ID,
            'FirstName': user.FirstName,
            'LastName': user.LastName,
            'DateOfBirth': user.DateOfBirth,
            'Email': user.Email,
            'Address': user.Address,
            'EmployeesList': user.EmployeesList,
            'Department': user.Department.to_dict() if user.Department else None,  # Assuming Department has to_dict()
            'Role': user.Role.value if isinstance(user.Role, ROLE) else user.Role
        }

    def _dict_to_user(self, data: dict) -> User:
        """Convert dictionary to User object"""
        # Reconstruct Department if it exists
        department = None
        if data.get('Department'):
            department = Department.from_dict(data['Department'])  # Assuming Department has from_dict()

        # Reconstruct Role
        role = ROLE(data.get('Role', ROLE.GUEST.value)) if data.get('Role') else ROLE.GUEST

        return User(
            ID=data.get('ID'),
            FirstName=data.get('FirstName'),
            LastName=data.get('LastName'),
            DateOfBirth=data.get('DateOfBirth'),
            Email=data.get('Email'),
            Address=data.get('Address'),
            EmployeesList=data.get('EmployeesList'),
            Department=department,
            Role=role
        )

    def _read(self) -> dict:
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def _write(self, data: dict):
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def codeToMangaer(self,manager : User,code):
        data = self._read()
        data[manager.Email] = code
        self._write(data)

    def get_all_code(self) -> List:
        
        
        data = self._read()
        return [{email: code} for email, code in data.items() if not isinstance(code, dict)]
