import streamlit as st
import requests

st.title("🐕 The Dog API Explorer")

# Load your API key from Streamlit Secrets
api_key = st.secrets["api_keys"]["dogapi"]
headers = {"x-api-key": api_key}

# Button to fetch a new dog
if st.button("Show me a dog!"):
    # Request a random dog image + breed info
    res = requests.get("https://api.thedogapi.com/v1/images/search", headers=headers)
    data = res.json()[0]

    # Display image
    st.image(data["url"], use_container_width=True)

    # If breed info exists, show details
    if "breeds" in data and data["breeds"]:
        breed = data["breeds"][0]
        st.subheader(breed["name"])
        st.markdown(f"**Temperament:** {breed.get('temperament', 'Unknown')}")
        st.markdown(f"**Life span:** {breed.get('life_span', 'Unknown')}")
        st.markdown(f"**Breed group:** {breed.get('breed_group', 'Unknown')}")
        st.markdown(f"**Origin:** {breed.get('origin', 'Unknown')}")
    else:
        st.info("No breed information found for this image 🐾")
else:
    st.info("Click the button to see a random dog 🐶")
