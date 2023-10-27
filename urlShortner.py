import streamlit as st
import hashlib
from datetime import datetime, timedelta

# Initialize a dictionary to store shortened URLs
shortened_urls = {}

# Custom short URL base
custom_short_url_base = "https://short.link/"

# Streamlit app layout settings
st.set_page_config(layout="wide")

# Function to generate a shortened URL
def shorten_url(original_url):
    # Generate a unique ID for the shortened URL (e.g., last 4 characters of the hash)
    url_id = hashlib.md5(original_url.encode()).hexdigest()[-8:-1]
    return f"{custom_short_url_base}{url_id}"

# Side menu for managing shortened URLs
menu_col = st.sidebar.container()

# Logo and app title within the menu
with menu_col:
    st.image("logo.svg")
    st.title("URL Shortener App")
    
    st.subheader("Shortened URLs")
    for url, data in shortened_urls.items():
        st.write(f"Shortened URL: {url}")
        if st.button(f"Delete {url}"):
            del shortened_urls[url]

# Main content area for creating and managing URLs
st.header("Create Short URL")

# Create Short URL form on the right side
main_col1, main_col2 = st.columns([3, 1])

original_url = main_col1.text_input("Enter the original URL:")
expiration_time = main_col1.selectbox("Expiration Time", ["1 minute","5 minutes", "10 minutes", "1 hour"])

# Calculate expiration time
if expiration_time == "1 minute":
    expiration_time = 1
if expiration_time == "5 minutes":
    expiration_time = 5
elif expiration_time == "10 minutes":
    expiration_time = 10
elif expiration_time == "1 hour":
    expiration_time = 60
else:
    expiration_time = 0

# Variable to store the generated short URL
generated_short_url = ""

if main_col1.button("Shorten URL", key="left_shorten_button"):
    if original_url:
        # Generate the shortened URL
        short_url = shorten_url(original_url)
        generated_short_url = short_url  # Store the generated short URL
        # Calculate the expiration time
        if expiration_time > 0:
            expiration = datetime.now() + timedelta(minutes=expiration_time)
        else:
            expiration = None

        # Store the shortened URL and its expiration time
        shortened_urls[short_url] = {
            "original_url": original_url,
            "expiration": expiration,
        }

        st.success(f"Shortened URL: {short_url}")

# Manage Short URLs section
st.header("Manage Short URLs")

# List of shortened URLs and delete option
for url, data in shortened_urls.items():
    st.write(f"Original URL: {data['original_url']}")
    st.write(f"Shortened URL: {url}")

    if data['expiration']:
        remaining_time = data['expiration'] - datetime.now()
        st.write(f"Expires in: {remaining_time}")

    if st.button(f"Delete {url}"):
        del shortened_urls[url]

# Display the shortened URLs, including the generated short URL
if generated_short_url:
    st.write("Shortened URLs:")
    st.write(f"Shortened URL: {generated_short_url}")
    st.write(shortened_urls)
