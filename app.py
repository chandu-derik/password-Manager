import streamlit as st
from new import Auth
from storage import Storage
from generator import PasswordGenerator
from email_generator import EmailGenerator

# ================= OBJECTS =================
auth = Auth()
store = Storage()
gen = PasswordGenerator()
email_gen = EmailGenerator()

st.set_page_config(page_title="Password Manager", page_icon="🔐")
st.title("🔐 Password Manager")

# ================= SESSION STATE INIT =================
defaults = {
    "logged_in": False,
    "auth_view": "Login",   # Login | Signup | ResetMaster
    "current_user": None,
    "master_password": None,
    "generated_password": None,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ================= HELPER: EMAIL UI =================
def email_input_ui():
    choice = st.radio(
        "Email option",
        ["Enter manually", "Generate email"],
        horizontal=True,
        key="email_choice"
    )

    # Manual email
    if choice == "Enter manually":
        st.session_state.generated_email = None
        return st.text_input("Email")

    # Generated email
    word = st.text_input("Word to include in email")

    if st.button("Generate Email"):
        if word:
            st.session_state.generated_email = email_gen.generate_random_email(word)

    if st.session_state.generated_email:
        st.code(st.session_state.generated_email)
        return st.session_state.generated_email

    return None




# ================= AUTH (LOGIN / SIGNUP / RESET) =================
if not st.session_state.logged_in:

    # -------- SWITCH BETWEEN AUTH VIEWS --------
    if st.session_state.auth_view in ("Login", "Signup"):
        st.radio(
            "Choose action",
            ["Login", "Signup"],
            horizontal=True,
            key="auth_radio"
        )
        st.session_state.auth_view = st.session_state.auth_radio

    # ---------- LOGIN ----------
    if st.session_state.auth_view == "Login":
        username = st.text_input("Username")
        login_password = st.text_input("Login Password", type="password")
        master_password = st.text_input("Master Password", type="password")

        if st.button("Login"):

                # 1️⃣ Check username
            if not auth.user_exists(username):
                st.error("❌ Username does not exist")

                # 2️⃣ Check login password
            elif not auth.verify_login(username, login_password):
                st.error("❌ Incorrect login password")

                # 3️⃣ Check master key
            elif not auth.verify_master(username, master_password):
                st.error("❌ Incorrect master key")

                # 4️⃣ All correct
            else:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.session_state.master_password = master_password
                st.success("Login successful!")
                st.rerun()


        st.markdown(" **Forgot your master key?**")
        if st.button("Reset Master Key"):
            st.session_state.auth_view = "ResetMaster"
            st.rerun()

    # ---------- SIGNUP ----------
    elif st.session_state.auth_view == "Signup":
        new_username = st.text_input("Choose Username")
        new_login_password = st.text_input("Choose Login Password", type="password")
        new_master_password = st.text_input("Choose Master Password", type="password")

        if st.button("Signup"):
            if not new_username or not new_login_password or not new_master_password:
                st.error("All fields are required")
            elif auth.streamlit_signup(new_username, new_login_password, new_master_password):
                st.success("Signup successful! Please login.")
                st.session_state.auth_view = "Login"
                st.rerun()
            else:
                st.error("User already exists")

    # ---------- RESET MASTER KEY ----------
    elif st.session_state.auth_view == "ResetMaster":
        st.subheader("Reset Master Key")

        st.warning(
            " This will permanently delete all saved passwords. "
            "They cannot be recovered."
        )

        username = st.text_input("Username")
        login_password = st.text_input("Login Password", type="password")
        new_master = st.text_input("New Master Password", type="password")
        confirm_master = st.text_input("Confirm New Master Password", type="password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Cancel"):
                st.session_state.auth_view = "Login"
                st.rerun()

        with col2:
            if st.button("Reset Vault"):
                if not username or not login_password or not new_master:
                    st.error("All fields are required")
                elif new_master != confirm_master:
                    st.error("Master passwords do not match")
                elif not auth.verify_login(username, login_password):
                    st.error("Login password is incorrect")
                else:
                    # 1️⃣ Clear vault
                    store.reset_vault(username)

                        # 2️⃣ Reset master key
                    auth.reset_master_key(username, new_master)

                        # 3️⃣ Clear session state (important)
                    st.session_state.logged_in = False
                    st.session_state.current_user = None
                    st.session_state.master_password = None

                        # 4️⃣ Success message
                    st.success(" Vault has been reset successfully. Please login with your new master key.")

                        # 5️⃣ Redirect to login
                    st.session_state.auth_view = "Login"
                    st.rerun()



# ================= DASHBOARD =================
else:
    st.subheader(f"Welcome, {st.session_state.current_user} 👋")

    option = st.selectbox(
        "Choose an action",
        [
            "Add Password (Manual)",
            "Generate Random Password",
            "Generate Special Password",
            "View Passwords",
            "Search by Website",
            "Delete Password",
            "Logout"
        ]
    )

    # ---------- MANUAL ----------
    if option == "Add Password (Manual)":
        website = st.text_input("Website")
        email = email_input_ui()
        password = st.text_input("Password")

        if st.button("Save Password") and email:
            store.File_storage(
                st.session_state.current_user,
                website,
                email,
                password,
                st.session_state.master_password
            )
            st.success("Password saved!")

    # ---------- RANDOM PASSWORD ----------
    elif option == "Generate Random Password":
        length = st.slider("Password Length", 4, 32, 12)

        if st.button("Generate"):
            st.session_state.generated_password = gen.generate_random_password(length)

        if st.session_state.generated_password:
            st.code(st.session_state.generated_password)

            website = st.text_input("Website")
            email = email_input_ui()

            if st.button("Save Generated Password") and email:
                store.File_storage(
                    st.session_state.current_user,
                    website,
                    email,
                    st.session_state.generated_password,
                    st.session_state.master_password
                )
                st.success("Password saved!")
                st.session_state.generated_password = None

    # ---------- SPECIAL PASSWORD ----------
    elif option == "Generate Special Password":
        length = st.slider("Length", 6, 32, 12)
        upper = st.checkbox("Uppercase", True)
        lower = st.checkbox("Lowercase", True)
        digits = st.checkbox("Digits", True)
        special = st.checkbox("Special Characters", True)
        word = st.text_input("Include a word (optional)")

        if st.button("Generate Special"):
            st.session_state.generated_password = gen.generate_custom_password(
                length, upper, lower, digits, special, word
            )

        if st.session_state.generated_password:
            st.code(st.session_state.generated_password)

            website = st.text_input("Website")
            email = email_input_ui()

            if st.button("Save Special Password") and email:
                store.File_storage(
                    st.session_state.current_user,
                    website,
                    email,
                    st.session_state.generated_password,
                    st.session_state.master_password
                )
                st.success("Password saved!")
                st.session_state.generated_password = None

    # ---------- VIEW ----------
    elif option == "View Passwords":
        records = store._get_user_passwords(
            st.session_state.current_user,
            st.session_state.master_password
        )

        if records:
            for i, (w, e, p) in enumerate(records, 1):
                st.write(f"{i}. **{w}** | {e} | `{p}`")
        else:
            st.info("No passwords saved")

    # ---------- SEARCH ----------
    elif option == "Search by Website":
        term = st.text_input("Search website")

        if term:
            records = store._get_user_passwords(
                st.session_state.current_user,
                st.session_state.master_password
            )

            matches = [(w, e, p) for w, e, p in records if term.lower() in w.lower()]

            if matches:
                for w, e, p in matches:
                    st.write(f"**{w}** | {e} | `{p}`")
            else:
                st.info("No matching website found")

    # ---------- DELETE ----------
    elif option == "Delete Password":
        records = store._get_user_passwords(
            st.session_state.current_user,
            st.session_state.master_password
        )

        if not records:
            st.info("No passwords to delete")
        else:
            websites = [w for w, _, _ in records]
            selected = st.selectbox("Select website", websites)

            if st.button("Delete Selected Password"):
                from crypto_utils import derive_key
                vault_file = store._vault_file(st.session_state.current_user)
                fernet = derive_key(st.session_state.master_password)

                new_lines = []
                with open(vault_file, "r") as f:
                    for line in f:
                        if "|" not in line:
                            new_lines.append(line)
                            continue
                        _, blob = line.strip().split("|", 1)
                        website, *_ = fernet.decrypt(blob.encode()).decode().split(",", 2)
                        if website != selected:
                            new_lines.append(line)

                with open(vault_file, "w") as f:
                    f.writelines(new_lines)

                st.success(f"Deleted password for {selected}")
                st.rerun()

    # ---------- LOGOUT ----------
    elif option == "Logout":
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.master_password = None
        st.session_state.generated_password = None
        st.session_state.auth_view = "Login"
        st.success("Logged out")
        st.rerun()