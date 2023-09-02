from dataclasses import dataclass
from hashlib import sha256
from typing import Optional


@dataclass
class Admin:
    id: int
    email: str
    password: Optional[str] = None

    @classmethod
    def from_session(cls, session: Optional[dict]) -> Optional["Admin"]:
        return cls(id=session["admin"]["id"], email=session["admin"]["email"])

    @staticmethod
    def hash_password(password: str) -> str:
        return sha256(password.encode()).hexdigest()

    def pass_valid_check(self, password: str) -> bool:
        return self.password == self.hash_password(password)
