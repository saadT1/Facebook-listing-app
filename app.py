import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import uuid
import platform
import bcrypt
from streamlit_option_menu import option_menu
from listing import listing
from data import data
from files import files
st.set_page_config(page_title="Facebook Listing app", page_icon="🌊 ")

def get_device_cred():
    return {
        "device_name": platform.node(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.architecture()[0],
        "machine": platform.machine(),
        "processor": platform.processor(),
        "device_id": str(uuid.getnode())
    }

def signup(db):
    st.subheader("Signup")
    username = st.text_input("Username", key="signup_username")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Register Device"):
        if not username or not password:
            st.error("❌ Please provide both username and password.")
        else:
            # Check if username already exists to prevent duplicates (optional enhancement)
            user_ref = db.collection("requests").document(username)
            if user_ref.get().exists:
                st.error("❌ Username already exists. Choose a different one.")
            else:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                device_cred = get_device_cred()
                device_cred['password_hash'] = hashed_password
                user_ref.set(device_cred, merge=True)
                st.success(f"✅ Registered successfully as {username}! You can now log in.")

def login(db):
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if not username or not password:
            st.error("❌ Please provide both username and password.")
        else:
            user_ref = db.collection("users").document(username)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_data = user_doc.to_dict()
                stored_password_hash = user_data.get("password_hash")
                stored_device_id = user_data.get("device_id")

                if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                    current_device_cred = get_device_cred()
                    current_device_id = current_device_cred.get("device_id")

                    if current_device_id == stored_device_id:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("✅ Login successful!")
                    else:
                        st.error("🚫 Device ID does not match. Access denied.")
                else:
                    st.error("❌ Incorrect password.")
            else:
                st.error("❌ User not found.")

def logout():
    st.session_state.authenticated = False
    st.success("Logged out successfully.")



def main():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate("facebook-auth-a2cfd-e4e8f9ae0994.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")
        return

    


    # Initialize session state if not already present
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = ""

# Authentication flow
    if not st.session_state.authenticated:
        choice = st.radio("Select an option:", ["Login", "Signup"], horizontal=True)
        if choice == "Login":
            login(db)  # Your login function
        else:
            signup(db)  # Your signup function
    else:
    # Sidebar when authenticated
        st.sidebar.title(f"Welcome, {st.session_state.username}!")
    
        page = st.sidebar.selectbox("Go to:", ["Dashboard", "Data", "Files","Logout"])

        if page == "Dashboard":
            st.title("Automation Section!")
            if st.button("Start Listing"):
                listing()
        elif page == "Data":
            data()
        elif page == "Files":
            files()
        elif page == "Logout":
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()
  

if __name__ == "__main__":
    main()