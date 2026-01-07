import hashlib
from new import Auth
from generator import PasswordGenerator
from email_generator import EmailGenerator
from storage import Storage

auth = Auth()
gen = PasswordGenerator()
email_gen = EmailGenerator()
store = Storage()


def main_menu():
    while True:
        print("\n==== PASSWORD MANAGER ====")
        print("1) Signup")
        print("2) Login")
        print("3) Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            auth.SignUp()

        elif choice == "2":
            if not auth.login():
                continue

            # 🔐 MASTER PASSWORD LOOP
            while True:
                master_password = input("Enter your master password: ")

                if auth.verify_master(auth.current_user, master_password):
                    # ✅ MASTER VERIFIED
                    user_menu(master_password)
                    break

                print("\n❌ Wrong master password.")
                option = input("1) Try again\n2) Reset vault\nChoose: ").strip()

                if option == "2":
                    store.reset_vault(auth.current_user)

                    new_master = input("Set NEW master password: ")
                    with open(f"users/{auth.current_user}/master.txt", "w") as f:
                        f.write(hashlib.sha256(new_master.encode()).hexdigest())

                    print("✅ Master password reset successfully.")
                    user_menu(new_master)
                    break

            # logout returns here
            auth.current_user = None

        elif choice == "3":
            print("You are out... BYE!!!!!")
            break

        else:
            print("Please enter a valid option")


def get_email_choice():
    choice = input("Do you want to generate an email? (yes/no): ").strip().lower()

    if choice == "yes":
        word = input("Enter a word to include in email: ").strip()
        email = email_gen.generate_random_email(word)
        print("Generated Email:", email)
        return email

    elif choice == "no":
        email = input("Enter existing email (or press Enter to skip): ").strip()
        return email if email else None

    return None


def user_menu(master_password):
    while True:
        print("\n==== USER MENU ====")
        print("1) Generate Random Password")
        print("2) Generate Special Password")
        print("3) View Saved Passwords")
        print("4) Delete Password")
        print("5) Search by Website")
        print("6) Logout")

        option = input("Choose the option: ").strip()

        if option == "1":
            email = get_email_choice()
            password = gen.random_password()

            if password:
                website = input("Enter the website name: ").strip().lower()
                store.File_storage(
                    auth.current_user,
                    website,
                    email,
                    password,
                    master_password
                )
                print("✅ Saved successfully!")

        elif option == "2":
            email = get_email_choice()
            values = gen.User_preferences()

            if values:
                password = gen.User_preference_password(*values)

                if password:
                    website = input("Enter the website name: ").strip().lower()
                    store.File_storage(
                        auth.current_user,
                        website,
                        email,
                        password,
                        master_password
                    )
                    print("✅ Saved successfully!")

        elif option == "3":
            store.view_passwords(auth.current_user, master_password)

        elif option == "4":
            store.delete_password_by_number(auth.current_user, master_password)

        elif option == "5":
            term = input("Enter website name to search: ").strip()
            store.search_by_website(auth.current_user, term, master_password)

        elif option == "6":
            print("🔒 Password locked. Logging out...")
            break

        else:
            print("Choose a valid option")


if __name__ == "__main__":
    main_menu()