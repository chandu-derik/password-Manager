import os
import hashlib

BASE_DIR = "users"

def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


class Auth:
    def __init__(self):
        self.current_user = None

    
    def user_exists(self, username):
        return os.path.exists(f"users/{username}")


    def SignUp(self):
        username = input("Enter your name: ").lower().strip()
        user_dir = os.path.join(BASE_DIR, username)

        if os.path.exists(user_dir):
            print(" User already exists! Please login.")
            return False

        login_password = input("Set login password: ")
        master_password = input("Set MASTER password: ")

        os.makedirs(user_dir)

        # save login password hash
        with open(os.path.join(user_dir, "auth.txt"), "w") as f:
            f.write(hash_text(login_password))

        # save master password hash
        with open(os.path.join(user_dir, "master.txt"), "w") as f:
            f.write(hash_text(master_password))

        # create empty vault
        open(os.path.join(user_dir, "vault.txt"), "w").close()

        print(" Signup successful!")
        return True

    def login(self):
        username = input("Enter your name: ").lower().strip()
        password = input("Enter your password: ")

        user_dir = os.path.join(BASE_DIR, username)

        if not os.path.exists(user_dir):
            print(" User does not exist")
            return False

        with open(os.path.join(user_dir, "auth.txt"), "r") as f:
            saved_hash = f.read().strip()

        if hash_text(password) == saved_hash:
            print(" Login successful!")
            self.current_user = username
            return True

        print("Invalid password")
        return False

    def verify_master(self, username, master_password):
        master_file = os.path.join(BASE_DIR, username, "master.txt")
        if not os.path.exists(master_file):
            return False

        with open(master_file, "r") as f:
            saved_hash = f.read().strip()

        return hash_text(master_password) == saved_hash
    
    def verify_login(self, username, password):
        user_dir = os.path.join(BASE_DIR, username)

        if not os.path.exists(user_dir):
            return False

        with open(os.path.join(user_dir, "auth.txt"), "r") as f:
            saved_hash = f.read().strip()

        if hash_text(password) == saved_hash:
            self.current_user = username
            return True

        return False
    
    def streamlit_signup(self, username, login_password, master_password):
        user_dir = os.path.join(BASE_DIR, username)

        if os.path.exists(user_dir):
            return False

        os.makedirs(user_dir)

        with open(os.path.join(user_dir, "auth.txt"), "w") as f:
            f.write(hash_text(login_password))

        with open(os.path.join(user_dir, "master.txt"), "w") as f:
            f.write(hash_text(master_password))

        open(os.path.join(user_dir, "vault.txt"), "w").close()

        return True
    
    def reset_master_key(self, username, new_master_password):
        user_dir = os.path.join(BASE_DIR, username)

        if not os.path.exists(user_dir):
            return False

        master_file = os.path.join(user_dir, "master.txt")

        with open(master_file, "w") as f:
            f.write(hash_text(new_master_password))

        return True




