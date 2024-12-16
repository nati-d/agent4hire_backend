from typing import Any, Dict


class User:
    """Class to represent a user."""

    def __init__(self, user_id: str, username: str, email: str, password: str):
        """
        Constructor for the User class.
        
        :param user_id: The ID of the user.
        :param username: The username of the user.
        :param email: The email address of the user.
        :param password: The password of the user.
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def from_dict(user_data: Dict[str, Any]) -> "User":
        return User(
            user_id=user_data["user_id"],
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"]
        )