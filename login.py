import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import uuid
import platform


if not firebase_admin._apps:
    cred = credentials.Certificate("facebook-auth-a2cfd-e4e8f9ae0994.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

def get_device_cred():
        return {
        "device_name": platform.node(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.architecture()[0],
        "machine": platform.machine(),
        "processor": platform.processor(),
        "device_id": str(uuid.getnode())  # Unique identifier
    }  # Unique device ID

def signup():
    st.subheader("Signup")
    username = st.text_input("Username")

    if st.button("Register Device"):
        user_ref = db.collection("requests").document(username)
        
        # Store full device information in Firestore
        user_ref.set(get_device_cred(), merge=True)  

        st.success(f"✅ Registered for {username}! Wait for the admin to approve the request.")





def login():
    st.subheader("Login")
    username = st.text_input("Username")

    if st.button("Login"):
        user_ref = db.collection("users").document(username)
        user_doc = user_ref.get()
    
        if user_doc.exists:
            user_data = user_doc.to_dict()
            stored_device_id = user_data.get("device_id")  # Now correctly fetching the string

            current_device_id = get_device_cred() # Get current device ID
            current_device_id = current_device_id["device_id"]
            # Compare stored device ID with the current one
            if stored_device_id == current_device_id:
                st.success("✅ Login successful!")
            else:
                st.error("🚫 Access denied! This account is locked to another device.")
        else:
            st.error("❌ User not found.")






# Logout function
def logout():
    st.session_state.authenticated = False
    st.success("Logged out successfully.")

# Main UI
st.title("User Authentication System")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    choice = st.radio("Select an option:", ["Login", "Signup"])
    if choice == "Login":
        login()
    else:
        signup()
else:
    st.subheader(f"Welcome, {st.session_state.username}!")
    if st.button("Logout"):
        logout()