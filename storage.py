import os
from crypto_utils import derive_key


class Storage:

    # ================= INTERNAL =================
    def _vault_file(self, user):
        return f"users/{user}/vault.txt"

    # ================= READ =================
    def _get_user_passwords(self, current_user, master_password):
        vault_file = self._vault_file(current_user)

        if not os.path.exists(vault_file):
            return []

        fernet = derive_key(master_password)
        records = []

        with open(vault_file, "r") as file:
            for line in file:
                line = line.strip()
                if "|" not in line:
                    continue

                _, encrypted_blob = line.split("|", 1)
                decrypted = fernet.decrypt(encrypted_blob.encode()).decode()
                website, email, password = decrypted.split(",", 2)
                records.append((website, email, password))

        return records

    # ================= WRITE =================
    def File_storage(self, current_user, website, email, password, master_password):
        fernet = derive_key(master_password)
        vault_file = self._vault_file(current_user)

        # Ensure user directory exists
        os.makedirs(os.path.dirname(vault_file), exist_ok=True)

        plain_text = f"{website},{email},{password}"
        encrypted_blob = fernet.encrypt(plain_text.encode()).decode()

        with open(vault_file, "a") as file:
            file.write(f"{current_user}|{encrypted_blob}\n")

    # ================= DELETE (STREAMLIT SAFE) =================
    def delete_password(self, current_user, website_to_delete, master_password):
        vault_file = self._vault_file(current_user)

        if not os.path.exists(vault_file):
            return False

        fernet = derive_key(master_password)
        new_lines = []

        with open(vault_file, "r") as file:
            for line in file:
                line = line.strip()
                if "|" not in line:
                    continue

                _, encrypted_blob = line.split("|", 1)
                decrypted = fernet.decrypt(encrypted_blob.encode()).decode()
                website, _, _ = decrypted.split(",", 2)

                if website != website_to_delete:
                    new_lines.append(line + "\n")

        with open(vault_file, "w") as file:
            file.writelines(new_lines)

        return True

    # ================= CLI HELPERS (OPTIONAL) =================
    def view_passwords(self, current_user, master_password):
        records = self._get_user_passwords(current_user, master_password)

        if not records:
            print("No saved passwords found.")
            return

        print("\nSaved Passwords:")
        for idx, (website, email, password) in enumerate(records, start=1):
            print(f"{idx}. Website: {website} | Email: {email} | Password: {password}")

    def search_by_website(self, current_user, term, master_password):
        records = self._get_user_passwords(current_user, master_password)

        matches = [
            (website, email, password)
            for website, email, password in records
            if term.lower() in website.lower()
        ]

        if not matches:
            print("No matching website found.")
            return

        print("\nSearch Results:")
        for idx, (website, email, password) in enumerate(matches, start=1):
            print(f"{idx}. Website: {website} | Email: {email} | Password: {password}")

    def delete_password_by_number(self, current_user, master_password):
        # CLI ONLY (not used by Streamlit)
        vault_file = self._vault_file(current_user)
        records = self._get_user_passwords(current_user, master_password)

        if not records:
            print("Nothing to delete.")
            return

        print("\nSaved Credentials:")
        for idx, (website, _, _) in enumerate(records, start=1):
            print(f"{idx}. {website}")

        choice = input("Enter the number to delete: ").strip()

        if not choice.isdigit():
            print("Invalid input.")
            return

        choice = int(choice)

        if choice < 1 or choice > len(records):
            print("Number out of range.")
            return

        website_to_delete = records[choice - 1][0]
        self.delete_password(current_user, website_to_delete, master_password)
        print(f"Password deleted for '{website_to_delete}'")

    def reset_vault(self, current_user):
        vault_file = self._vault_file(current_user)
        open(vault_file, "w").close()
