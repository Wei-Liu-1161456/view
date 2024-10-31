import pickle
from typing import Optional

class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

class UserModel:
    def __init__(self, filename: str = 'users.pkl'):
        self.filename = filename

    def save_user(self, user: User):
        """Save user data to a pickle file."""
        try:
            with open(self.filename, 'ab') as file:
                pickle.dump(user, file)
            print(f"User {user.name} saved to {self.filename}")
        except Exception as e:
            print(f"Error saving user: {e}")

    def load_user(self, user_id: int) -> Optional[User]:
        """Load a user by ID from the pickle file."""
        try:
            with open(self.filename, 'rb') as file:
                while True:
                    try:
                        user = pickle.load(file)
                        if user.user_id == user_id:
                            return user
                    except EOFError:
                        break
        except FileNotFoundError:
            print(f"No data found in {self.filename}")
        return None