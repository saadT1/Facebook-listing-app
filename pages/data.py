import streamlit as st
import json
import os

st.set_page_config(
    layout="wide",
    page_title="User Data Management",
)
# Define the file path
FILE_PATH = 'ids.json'

# Load existing data or create a new file
def load_data():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            return json.load(file)
    else:
        return {}

# Save data to the JSON file
def save_data(data):
    with open(FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

# Main function to render the Streamlit app
def main():
    st.title("User Data Management")

    # Initialize session state variables
    if 'edit_key' not in st.session_state:
        st.session_state['edit_key'] = None
    if 'delete_key' not in st.session_state:
        st.session_state['delete_key'] = None

    # Load data from file
    data = load_data()

    # User input for new entry
    st.subheader("Add New Entry")
    new_key = st.text_input("Key (e.g., email or phone number)", key="new_key")
    new_password = st.text_input("Password", key="new_password")
    new_location = st.text_input("Location", key="new_location")

    if st.button("Add Entry"):
        if new_key and new_password and new_location:
            data[new_key] = {
                "password": new_password,
                "location": new_location
            }
            save_data(data)
            # Use st.rerun() to refresh the app
            st.rerun()
        else:
            st.error("All fields are required to add a new entry.")

    # Data display inside an expander
    with st.expander("View Current Data", expanded=True):  # Expand the expander by default
        # Display existing data with column headers
        st.subheader("Current Data")
        
        # Create column headers
        header_cols = st.columns([6, 5, 5, 3, 3])  # Adjusted the column width ratios
        header_cols[0].write("**Key**")
        header_cols[1].write("**Password**")
        header_cols[2].write("**Location**")
        header_cols[3].write("**Edit**")
        header_cols[4].write("**Delete**")

        # Display data rows
        keys = list(data.keys())
        for idx, key in enumerate(keys):
            value = data[key]
            # Display data in columns with adjusted widths
            cols = st.columns([6, 5, 5, 3, 3])  # Adjusted the column width ratios
            cols[0].write(key)
            cols[1].write(value['password'])
            cols[2].write(value['location'])
            with cols[3]:
                # Edit button
                if st.button(f"Edit {idx}"):
                    st.session_state['edit_key'] = key
                    # Use st.rerun() to refresh the app
                    st.rerun()
            with cols[4]:
                # Delete button
                if st.button(f"Delete {idx}"):
                    st.session_state['delete_key'] = key
                    # Use st.rerun() to refresh the app
                    st.rerun()

    # Handle Edit Entry
    if st.session_state['edit_key'] is not None:
        key = st.session_state['edit_key']
        st.subheader(f"Edit Entry: {key}")
        new_password = st.text_input("Password", data[key]['password'], key='edit_password')
        new_location = st.text_input("Location", data[key]['location'], key='edit_location')

        if st.button("Save Changes"):
            data[key]['password'] = new_password
            data[key]['location'] = new_location
            save_data(data)
            st.session_state['edit_key'] = None  # Clear the edit key to close the edit section
            # Use st.rerun() to refresh the app
            st.rerun()

        if st.button("Cancel Edit"):
            st.session_state['edit_key'] = None  # Cancel the edit
            # Use st.rerun() to refresh the app
            st.rerun()

    # Handle Delete Entry
    if st.session_state['delete_key'] is not None:
        key = st.session_state['delete_key']
        st.warning(f"Are you sure you want to delete the entry: **{key}**?")
        if st.button("Yes, Delete"):
            del data[key]
            save_data(data)
            st.success(f"Entry {key} deleted successfully!")
            st.session_state['delete_key'] = None  # Clear the delete key
            # Use st.rerun() to refresh the app
            st.rerun()
        if st.button("Cancel"):
            st.session_state['delete_key'] = None  # Cancel the delete
            # Use st.rerun() to refresh the app
            st.rerun()

if __name__ == "__main__":
    main()
