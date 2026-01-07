import random
import string


class PasswordGenerator:

    # ===================== CLI METHODS (DO NOT USE IN STREAMLIT) =====================

    def random_password(self):
        length = int(input("Enter the password length : "))

        if length < 4:
            print("length must be greater than 3 to include all the characters")
            return

        while True:
            upper = random.choice(string.ascii_uppercase)
            lower = random.choice(string.ascii_lowercase)
            digit = random.choice(string.digits)
            special = random.choice(string.punctuation)

            password_length = length - 4
            all_characters = (
                string.ascii_lowercase +
                string.digits +
                string.ascii_uppercase +
                string.punctuation
            )

            remaining_password = [
                random.choice(all_characters)
                for _ in range(password_length)
            ]

            password_list = [upper, lower, digit, special] + remaining_password
            random.shuffle(password_list)

            password = "".join(password_list)
            print(f"Your Random password : {password}")

            choice = input(
                "\n1) Keep this password\n2) Generate another\nChoose: "
            ).strip()

            if choice == "1":
                return password
            elif choice == "2":
                continue
            else:
                print("Invalid choice")

    def User_preferences(self):
        try:
            length = int(input("Enter the password length : "))
        except ValueError:
            print("Please enter a valid number")
            return None

        Upper = input("Include Uppercase [yes/no] ? : ").strip().lower() == "yes"
        Lower = input("Include Lowercase [yes/no] ? : ").strip().lower() == "yes"
        Digit = input("Include Digit [yes/no] ? : ").strip().lower() == "yes"
        special = input("Include Special Characters [yes/no] ? : ").strip().lower() == "yes"

        word = input("Enter a word to include (optional) : ")

        if not (Upper or Lower or Digit or special):
            Upper = Lower = Digit = special = True

        return length, Upper, Lower, Digit, special, word

    def User_preference_password(self, length, Upper, Lower, Digit, special, word):
        if word and length < len(word):
            print("Required password length is less than the word")
            return None

        remaining_length = length - len(word)
        password_freq = ""
        required_password = []

        if Upper:
            required_password.append(random.choice(string.ascii_uppercase))
            password_freq += string.ascii_uppercase
        if Lower:
            required_password.append(random.choice(string.ascii_lowercase))
            password_freq += string.ascii_lowercase
        if Digit:
            required_password.append(random.choice(string.digits))
            password_freq += string.digits
        if special:
            required_password.append(random.choice(string.punctuation))
            password_freq += string.punctuation

        if not password_freq:
            password_freq = string.ascii_letters + string.digits + string.punctuation

        if remaining_length < len(required_password):
            print("The password cannot be created because of length mismatch!")
            return None

        remaining_chars = required_password[:]

        for _ in range(remaining_length - len(required_password)):
            remaining_chars.append(random.choice(password_freq))

        random.shuffle(remaining_chars)

        final_password = word + "".join(remaining_chars)
        print(f"\nHere is your special password : {final_password}")

        return final_password

    # ===================== STREAMLIT SAFE METHODS =====================

    def generate_random_password(self, length):
        """
        Streamlit-safe random password generator
        """
        if length < 4:
            return None

        upper = random.choice(string.ascii_uppercase)
        lower = random.choice(string.ascii_lowercase)
        digit = random.choice(string.digits)
        special = random.choice(string.punctuation)

        remaining = length - 4
        all_chars = string.ascii_letters + string.digits + string.punctuation

        remaining_chars = [
            random.choice(all_chars)
            for _ in range(remaining)
        ]

        password_list = [upper, lower, digit, special] + remaining_chars
        random.shuffle(password_list)

        return "".join(password_list)

    def generate_custom_password(self, length, Upper, Lower, Digit, special, word=""):
        """
        Streamlit-safe custom password generator
        """
        if word and length < len(word):
            return None

        remaining_length = length - len(word)
        pool = ""
        required = []

        if Upper:
            required.append(random.choice(string.ascii_uppercase))
            pool += string.ascii_uppercase
        if Lower:
            required.append(random.choice(string.ascii_lowercase))
            pool += string.ascii_lowercase
        if Digit:
            required.append(random.choice(string.digits))
            pool += string.digits
        if special:
            required.append(random.choice(string.punctuation))
            pool += string.punctuation

        if not pool:
            pool = string.ascii_letters + string.digits + string.punctuation

        if remaining_length < len(required):
            return None

        remaining_chars = required[:]

        for _ in range(remaining_length - len(required)):
            remaining_chars.append(random.choice(pool))

        random.shuffle(remaining_chars)

        return word + "".join(remaining_chars)
