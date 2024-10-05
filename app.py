import streamlit as st
import uuid
import hashlib

def generate_license_key(device_id):
    # Hash the device ID to generate a license key
    license_key = hashlib.sha256(device_id.encode()).hexdigest()
    return license_key

def verify_license_key(input_key, device_id):
    # Generate a license key from the device ID and compare it with the input key
    expected_key = generate_license_key(device_id)
    return input_key == expected_key

# Streamlit app
def main():
    st.title("License Key Generator and Verification")

    # Input fields for user details
    full_name = st.text_input("Full Name")
    mobile_number = st.text_input("Mobile Number")
    email_address = st.text_input("Email Address")

    # Button to generate license key
    if st.button("Generate License Key"):
        if full_name and mobile_number and email_address:
            # Get the unique device ID (MAC address)
            device_id = str(uuid.getnode())

            # Generate the license key
            license_key = generate_license_key(device_id)

            # Display user information and license key
            st.success(f"Full Name: {full_name}")
            st.success(f"Mobile Number: {mobile_number}")
            st.success(f"Email Address: {email_address}")
            st.success(f"Generated License Key: {license_key}")
        else:
            st.error("Please fill in all the fields.")

    # Input field for license key verification
    st.subheader("Verify License Key")
    input_key = st.text_input("Enter License Key to Verify")

    # Button to verify license key
    if st.button("Verify License Key"):
        if input_key:
            # Get the unique device ID (MAC address)
            device_id = str(uuid.getnode())

            # Verify the input license key
            if verify_license_key(input_key, device_id):
                st.success("License Key is valid.")
            else:
                st.error("Invalid License Key.")
        else:
            st.error("Please enter a license key to verify.")

if __name__ == "__main__":
    main()