import streamlit as st
import pandas as pd

# Dummy credentials for the purpose of this example
USERNAME = "APL41051"
PASSWORD = "APL41051"

# Function to handle login
def login():
    st.session_state["authenticated"] = False
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state["authenticated"] = True
            st.session_state["logged_out"] = False  # Reset logout state on login
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# Function to merge Excel files without column intersection, concatenating all data
def merge_excel_files(file_list):
    merged_df = pd.DataFrame()

    for uploaded_file in file_list:
        try:
            # Load the Excel file
            xls = pd.ExcelFile(uploaded_file)
            # Iterate through each sheet in the Excel file
            for sheet in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet)

                # Concatenate all files' data, even if columns differ
                merged_df = pd.concat([merged_df, df], ignore_index=True)

        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")

    return merged_df

# Custom CSS for background color
page_bg_color = """
<style>
    body {
        background-color: #FFB6C1;
    }
    .stApp {
        background-color: #B0E0E6;
    }
</style>
"""

# Apply the background color
st.markdown(page_bg_color, unsafe_allow_html=True)

# Check if user is authenticated
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "logged_out" not in st.session_state:
    st.session_state["logged_out"] = False  # To track logout state

# Logout success message handling
if st.session_state["logged_out"]:
    st.success("You have successfully logged out.")
    st.session_state["logged_out"] = False  # Clear the logout state to prevent message persistence
    st.stop()  # Prevent further execution

if not st.session_state["authenticated"]:
    login()
else:
    # Streamlit App after login
    st.title("Excel Files Merger")

    # Logout button
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["logged_out"] = True  # Set logout flag
        st.experimental_rerun()  # Rerun the app and go back to the login page

    # File uploader
    uploaded_files = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)

    if uploaded_files:
        # Merge the files when the user uploads them
        merged_data = merge_excel_files(uploaded_files)

        if not merged_data.empty:
            # Display the merged data
            st.write("Merged Data:")
            st.dataframe(merged_data)

            # Provide a download link for the merged Excel file
            output_file = "merged_output.xlsx"
            merged_data.to_excel(output_file, index=False)

            with open(output_file, "rb") as f:
                st.download_button(
                    label="Download Merged Excel",
                    data=f,
                    file_name="merged_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.warning("No data to merge.")
