import json
from typing import Optional

class JsonUserPasswordStore:
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

    def set_password(self, userid: str, hashed_password: str):
        data = self._read()
        data[userid] = hashed_password
        self._write(data)

    def get_password(self, userid: str) -> Optional[str]:
        data = self._read()
        return data.get(userid)

    def _read(self):
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def _write(self, data):
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)

