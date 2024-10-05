import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(
    layout="wide",
    page_title="User Data and Furniture Listings Management",
)

# Define file paths
USER_DATA_FILE_PATH = 'ids.json'
LISTINGS_DATA_FILE_PATH = 'data.json'

# User Data Management Functions

# Load existing data or create a new file
def load_user_data():
    if os.path.exists(USER_DATA_FILE_PATH):
        with open(USER_DATA_FILE_PATH, 'r') as file:
            return json.load(file)
    else:
        return {}

# Save data to the JSON file
def save_user_data(data):
    with open(USER_DATA_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

# Furniture Listings Management Functions

# Load existing listings data or initialize an empty dictionary
def load_listings_data():
    if os.path.exists(LISTINGS_DATA_FILE_PATH):
        with open(LISTINGS_DATA_FILE_PATH, 'r') as file:
            return json.load(file)
    else:
        return {"listings": {}}

# Save listings data to the JSON file
def save_listings_data(data):
    with open(LISTINGS_DATA_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    st.title("User Data and Furniture Listings Management")

    # Create tabs for User Data Management and Furniture Listings Manager
    tab1, tab2 = st.tabs(["User Data Management", "Furniture Listings Manager"])

    # User Data Management Tab
    with tab1:
        # Initialize session state variables for user data
        if 'edit_key' not in st.session_state:
            st.session_state['edit_key'] = None
        if 'delete_key' not in st.session_state:
            st.session_state['delete_key'] = None

        # Load user data from file
        user_data = load_user_data()

        # User input for new entry inside a form with clear_on_submit=True
        st.subheader("Add New User Entry")
        with st.form(key='add_user_form', clear_on_submit=True):
            new_key = st.text_input("Key (e.g., email or phone number)")
            new_password = st.text_input("Password")
            new_location = st.text_input("Location")
            submit_button = st.form_submit_button(label='Add User Entry')

        if submit_button:
            if new_key and new_password and new_location:
                user_data[new_key] = {
                    "password": new_password,
                    "location": new_location
                }
                save_user_data(user_data)
                st.success("User entry added successfully.")
                # No need to reset input fields; they are cleared automatically
                # Use st.rerun() to refresh the app if needed
                st.rerun()
            else:
                st.error("All fields are required to add a new entry.")

        # Data display inside an expander
        with st.expander("View Current User Data", expanded=True):
            # Display existing data with column headers
            st.subheader("Current User Data")
            
            # Create column headers
            header_cols = st.columns([6, 5, 5, 3, 3])
            header_cols[0].write("**Key**")
            header_cols[1].write("**Password**")
            header_cols[2].write("**Location**")
            header_cols[3].write("**Edit**")
            header_cols[4].write("**Delete**")

            # Display data rows
            keys = list(user_data.keys())
            for idx, key in enumerate(keys):
                value = user_data[key]
                # Display data in columns with adjusted widths
                cols = st.columns([6, 5, 5, 3, 3])
                cols[0].write(key)
                cols[1].write(value['password'])
                cols[2].write(value['location'])
                with cols[3]:
                    # Edit button
                    if st.button(f"Edit {idx}", key=f"user_edit_{idx}"):
                        st.session_state['edit_key'] = key
                        st.rerun()
                with cols[4]:
                    # Delete button
                    if st.button(f"Delete {idx}", key=f"user_delete_{idx}"):
                        st.session_state['delete_key'] = key
                        st.rerun()

        # Handle Edit Entry
        if st.session_state['edit_key'] is not None:
            key = st.session_state['edit_key']
            st.subheader(f"Edit User Entry: {key}")
            with st.form(key='edit_user_form'):
                new_password = st.text_input("Password", user_data[key]['password'])
                new_location = st.text_input("Location", user_data[key]['location'])
                save_changes = st.form_submit_button(label='Save Changes')
                cancel_edit = st.form_submit_button(label='Cancel Edit')

            if save_changes:
                user_data[key]['password'] = new_password
                user_data[key]['location'] = new_location
                save_user_data(user_data)
                st.session_state['edit_key'] = None
                st.success("Changes saved successfully.")
                st.rerun()

            if cancel_edit:
                st.session_state['edit_key'] = None
                st.rerun()

        # Handle Delete Entry
        if st.session_state['delete_key'] is not None:
            key = st.session_state['delete_key']
            st.warning(f"Are you sure you want to delete the user entry: **{key}**?")
            if st.button("Yes, Delete", key='confirm_user_delete'):
                del user_data[key]
                save_user_data(user_data)
                st.success(f"User entry {key} deleted successfully!")
                st.session_state['delete_key'] = None
                st.rerun()
            if st.button("Cancel", key='cancel_user_delete'):
                st.session_state['delete_key'] = None
                st.rerun()

    # Furniture Listings Manager Tab
    with tab2:
        # Initialize session state for listing input fields if not already done
        if 'edit_listing' not in st.session_state:
            st.session_state['edit_listing'] = False

        # Load listings data
        listings_data = load_listings_data()

        # Input section for adding new listings inside a form with clear_on_submit=True
        st.subheader("Add or Edit a Listing")
        with st.form(key='add_listing_form', clear_on_submit=True):
            category = st.text_input("Enter Category (e.g., beds, sofas, wardrobes, etc.)").strip()
            listing_name = st.text_input("Listing Name").strip()
            title = st.text_input("Title").strip()
            price = st.text_input("Price").strip()
            reference_category = st.text_input("Enter Reference Category (e.g., beds, sofas, etc.)").strip()
            description = st.text_area("Description").strip()
            id_ = st.text_input("ID").strip()
            id1 = st.text_input("ID1").strip()
            no_of_listings = st.text_input("No of Listings (comma-separated)").strip()
            submit_listing = st.form_submit_button(label='Add/Update Listing')

        if submit_listing:
            if category and listing_name:
                # Parse the 'no of listings' as a list of integers
                try:
                    no_of_listings_list = [int(num.strip()) for num in no_of_listings.split(',') if num.strip().isdigit()]
                except ValueError:
                    st.error("Invalid input for 'No of Listings'. Please enter comma-separated integers.")
                else:
                    # Ensure category exists in listings_data
                    if category not in listings_data['listings']:
                        listings_data['listings'][category] = {}
                    
                    # Add or update the listing
                    listings_data['listings'][category][listing_name] = {
                        "reference_category": reference_category,
                        "no of listings": no_of_listings_list,
                        "title": title,
                        "price": price,
                        "category": category,
                        "description": description,
                        "path": "",
                        "id": id_,
                        "id1": id1
                    }
                    # Save to file
                    save_listings_data(listings_data)
                    st.success(f"{listing_name} added/updated in {category}.")
                    # No need to reset input fields; they are cleared automatically
                    st.rerun()
            else:
                st.error("Category and Listing Name are required fields.")

        # Display all listings in a column-wise format and make them editable
        st.subheader("All Listings")

        all_listings = []
        for cat, items in listings_data['listings'].items():
            for name, details in items.items():
                listing_info = {
                    "Category": cat,
                    "Reference Category": details.get("reference_category", ""),
                    "Listing Name": name,
                    "No of Listings": ", ".join(map(str, details["no of listings"])),
                    "Title": details["title"],
                    "Price": details["price"],
                    "Description": details["description"],
                    "ID": details["id"],
                    "ID1": details["id1"]
                }
                all_listings.append(listing_info)

        if all_listings:
            # Convert to DataFrame for display
            df = pd.DataFrame(all_listings)

            # Editable DataFrame using st.data_editor
            edited_df = st.data_editor(df, num_rows="dynamic")

            # Check if the DataFrame has been edited
            if not df.equals(edited_df):
                st.info("You have made changes to the listings. Click 'Save Changes' to update.")
                if st.button("Save Changes"):
                    # Update listings_data with the edited DataFrame
                    updated_listings = {}
                    for _, row in edited_df.iterrows():
                        category = row["Category"]
                        listing_name = row["Listing Name"]
                        if category not in updated_listings:
                            updated_listings[category] = {}

                        # Try to parse 'No of Listings' as integers
                        try:
                            no_of_listings_list = [int(num.strip()) for num in row["No of Listings"].split(',') if num.strip().isdigit()]
                        except ValueError:
                            st.error(f"Invalid input for 'No of Listings' in {listing_name}. Please enter comma-separated integers.")
                            continue  # Skip this listing if there's an error

                        # Update the listing data
                        updated_listings[category][listing_name] = {
                            "reference_category": row["Reference Category"],
                            "no of listings": no_of_listings_list,
                            "title": row["Title"],
                            "price": row["Price"],
                            "category": category,
                            "description": row["Description"],
                            "path": "",
                            "id": row["ID"],
                            "id1": row["ID1"]
                        }

                    # Save changes to listings_data
                    listings_data['listings'] = updated_listings

                    # Save changes to file
                    save_listings_data(listings_data)
                    st.success("Listings updated successfully.")
                    st.rerun()

            # Delete all entries button
            if st.button("Delete All Listings"):
                listings_data = {"listings": {}}
                # Save the cleared data to file
                save_listings_data(listings_data)
                st.success("All listings deleted.")
                st.rerun()
        else:
            st.write("No listings available.")

if __name__ == "__main__":
    main()
