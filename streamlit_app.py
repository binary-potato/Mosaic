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
        json.dump({"threads": [], "messages": []}, f)

# Load data from JSON file
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# App layout
st.title("4chan-like Environment with Streamlit")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Direct Messages", "Search"])

# Category and subcategory selection
categories = {
    "Art": ["Digital Art", "Traditional Art"],
    "Videos": ["Gaming", "Music"],
    "Photos": ["Nature", "Urban"],
    "Programming": ["Python", "JavaScript"],
    "Communities": ["Animal Community", "Gaming Community"]
}

# Home Page
if page == "Home":
    st.subheader("Home")

    # Select category and subcategory
    selected_category = st.selectbox("Select a category", list(categories.keys()))
    if selected_category in categories:
        selected_subcategory = st.selectbox("Select a subcategory", categories[selected_category])
    else:
        selected_subcategory = None

    # Display threads for the selected category and subcategory
    st.subheader(f"{selected_category} - {selected_subcategory} Threads")
    data = load_data()
    threads = [thread for thread in data['threads'] if thread['category'] == selected_category and thread['subcategory'] == selected_subcategory]

    for thread in threads:
        st.write(f"**{thread['title']}**")
        st.write(thread['content'])
        if thread['image']:
            st.image(thread['image'], use_column_width=True)
        st.write("---")

    # Create new thread
    st.subheader("Create New Thread")
    with st.form("thread_form"):
        title = st.text_input("Title")
        content = st.text_area("Content")
        image = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
        submit = st.form_submit_button("Submit")

        if submit:
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

# Direct Messages Page
elif page == "Direct Messages":
    st.subheader("Direct Messages")

    # Load messages
    data = load_data()
    messages = data['messages']

    # Display messages
    for message in messages:
        st.write(f"**From:** {message['sender']}")
        st.write(f"**To:** {message['receiver']}")
        st.write(f"**Message:** {message['content']}")
        st.write("---")

    # Send a new message
    st.subheader("Send a Message")
    with st.form("message_form"):
        sender = st.text_input("Your Name")
        receiver = st.text_input("Recipient's Name")
        content = st.text_area("Message")
        submit = st.form_submit_button("Send")

        if submit:
            if sender and receiver and content:
                new_message = {
                    "id": str(uuid4()),
                    "sender": sender,
                    "receiver": receiver,
                    "content": content
                }
                data['messages'].append(new_message)
                save_data(data)
                st.success("Message sent successfully!")
            else:
                st.warning("Please fill in all fields.")

# Search Page
elif page == "Search":
    st.subheader("Search")

    # Search bar
    search_query = st.text_input("Search for threads")
    if search_query:
        data = load_data()
        threads = [thread for thread in data['threads'] if search_query.lower() in thread['title'].lower() or search_query.lower() in thread['content'].lower()]

        if threads:
            st.write(f"**Search results for '{search_query}':**")
            for thread in threads:
                st.write(f"**{thread['title']}**")
                st.write(thread['content'])
                if thread['image']:
                    st.image(thread['image'], use_column_width=True)
                st.write("---")
        else:
            st.warning("No threads found matching your search.")

# Code sharing and execution
st.sidebar.subheader("Share and Run Code")
code = st.sidebar.text_area("Enter your code")
if st.sidebar.button("Run Code"):
    if code:
        # Encode the code to make it URL-safe
        encoded_code = urllib.parse.quote(code)
        link = f"https://myide.created.app?code={encoded_code}"
        st.sidebar.write(f"[Click here to run the code]({link})")
    else:
        st.sidebar.warning("Please enter some code.")
