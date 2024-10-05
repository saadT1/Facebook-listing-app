import os
import streamlit as st

# Streamlit input to get folder path from user
st.title('Batch File Renamer')
folder_path = r'' + st.text_input('Enter the path of the folder:', '')

# Button to start renaming files
if st.button('Rename Files') and folder_path:
    try:
        # List all files in the folder
        files = os.listdir(folder_path)

        # Filter out directories, keep only files
        files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]

        # Sort files to ensure consistent ordering
        files.sort()

        # Iterate over the files and rename them
        for index, file_name in enumerate(files, start=1):
            # Construct the full file path
            old_file_path = os.path.join(folder_path, file_name)
            
            # Define the new file name
            new_file_name = f" {index}{os.path.splitext(file_name)[1]}"
            
            # Construct the new file path
            new_file_path = os.path.join(folder_path, new_file_name)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)

        st.success("All files have been renamed sequentially.")
        st.write("Renamed files:")
        for file in files:
            st.write(file)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Button to change file extensions to .jpg
if st.button('Change Extensions to .jpg') and folder_path:
    try:
        updated_files = []
        for filename in os.listdir(folder_path):
            # Create the full file path
            file_path = os.path.join(folder_path, filename)
            
            # Check if it's a file (not a directory)
            if os.path.isfile(file_path):
                # Split the filename into name and extension
                file_base, file_extension = os.path.splitext(filename)
                
                # Only change the extension if it's not already .jpg
                if file_extension.lower() != '.jpg':
                    new_filename = file_base + '.jpg'
                    new_file_path = os.path.join(folder_path, new_filename)
                    
                    # Rename the file
                    os.rename(file_path, new_file_path)
                    updated_files.append(new_filename)
                    st.info(f'Renamed: {filename} -> {new_filename}')
        st.success("All file extensions have been changed to .jpg.")
        st.write("Files with updated extensions:")
        for updated_file in updated_files:
            st.write(updated_file)
    except Exception as e:
        st.error(f"An error occurred: {e}")