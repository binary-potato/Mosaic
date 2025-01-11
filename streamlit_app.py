import streamlit as st
import json
import os
from uuid import uuid4
from PIL import Image
import urllib.parse

# File to store data
DATA_FILE = 'data.json'

# Initialize data if the file doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"categories": {}, "threads": [], "messages": []}, f)

# Load data from JSON file
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Load categories and subcategories
data = load_data()
categories = data.get("categories", {})

# Sidebar for navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.selectbox("Go to", ["Home", "Messages", "Search", "Create Subcategory"])

# Home Page
if selected_page == "Home":
    st.title("Welcome to the Community")
    st.write("Hi there, what would you like to do?")
    
    # Options
    option = st.selectbox("Choose an action", ["Create a Thread", "Message a Friend", "Search for a Topic", "Create a Subcategory"])
    
    if option == "Create a Thread":
        st.subheader("Create New Thread")
        selected_category = st.selectbox("Select a category", list(categories.keys()))
        if selected_category in categories:
            selected_subcategory = st.selectbox("Select a subcategory", categories[selected_category])
        else:
            selected_subcategory = None
        title = st.text_input("Title")
        content = st.text_area("Content")
        image = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
        if st.button("Submit"):
            if title and content:
                new_thread = {
                    "id": str(uuid4()),
                    "category": selected_category,
                    "subcategory": selected_subcategory,
                    "title": title,
                    "content": content,
                    "image": None
                }
                if image:
                    img = Image.open(image)
                    img_path = f"images/{new_thread['id']}.{image.type.split('/')[-1]}"
                    os.makedirs("images", exist_ok=True)
                    img.save(img_path)
                    new_thread['image'] = img_path
                data['threads'].append(new_thread)
                save_data(data)
                st.success("Thread created successfully!")
            else:
                st.warning("Please fill in the title and content.")
    
    # Placeholder for other options
    elif option == "Message a Friend":
        st.subheader("Message a Friend")
        # Message form here
    
    elif option == "Search for a Topic":
        st.subheader("Search for a Topic")
        # Search form here
    
    elif option == "Create a Subcategory":
        st.subheader("Create a Subcategory")
        selected_category = st.selectbox("Select a category to add subcategory", list(categories.keys()))
        new_subcategory = st.text_input("New Subcategory Name")
        if st.button("Add Subcategory"):
            if new_subcategory:
                if new_subcategory not in categories.get(selected_category, []):
                    categories[selected_category].append(new_subcategory)
                    data['categories'] = categories
                    save_data(data)
                    st.success(f"Subcategory '{new_subcategory}' added to '{selected_category}'.")
                else:
                    st.warning(f"Subcategory '{new_subcategory}' already exists in '{selected_category}'.")
            else:
                st.warning("Please enter a subcategory name.")

# Messages Page
elif selected_page == "Messages":
    st.subheader("Messages")
    # Display messages here

# Search Page
elif selected_page == "Search":
    st.subheader("Search")
    search_query = st.text_input("Search for threads")
    if search_query:
        # Search functionality here
        pass

# Create Subcategory Page
elif selected_page == "Create Subcategory":
    st.subheader("Create a Subcategory")
    selected_category = st.selectbox("Select a category to add subcategory", list(categories.keys()))
    new_subcategory = st.text_input("New Subcategory Name")
    if st.button("Add Subcategory"):
        if new_subcategory:
            if new_subcategory not in categories.get(selected_category, []):
                categories[selected_category].append(new_subcategory)
                data['categories'] = categories
                save_data(data)
                st.success(f"Subcategory '{new_subcategory}' added to '{selected_category}'.")
            else:
                st.warning(f"Subcategory '{new_subcategory}' already exists in '{selected_category}'.")
        else:
            st.warning("Please enter a subcategory name.")

# Code sharing and execution
st.sidebar.subheader("Share and Run Code")
code = st.sidebar.text_area("Enter your code")
if st.sidebar.button("Run Code"):
    if code:
        encoded_code = urllib.parse.quote(code)
        link = f"https://myide.created.app?code={encoded_code}"
        st.sidebar.write(f"[Click here to run the code]({link})")
    else:
        st.sidebar.warning("Please enter some code.")
