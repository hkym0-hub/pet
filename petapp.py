import streamlit as st
import requests

st.title("🐾 The Dog API Explorer")

# Load API key from secrets
api_key = st.secrets["api_keys"]["dogapi"]
headers = {"x-api-key": api_key}

# Fetch all breeds (once)
@st.cache_data
def get_breeds():
    res = requests.get("https://api.thedogapi.com/v1/breeds", headers=headers)
    return res.json()

breeds = get_breeds()
breed_names = [b["name"] for b in breeds]

# Breed selector
selected_breed = st.selectbox("Choose a breed:", breed_names)

if st.button("Show me this dog!"):
    # Find breed ID for the selected breed
    breed_id = next(b["id"] for b in breeds if b["name"] == selected_breed)
    
    # Request an image from that specific breed
    url = f"https://api.thedogapi.com/v1/images/search?breed_id={breed_id}"
    res = requests.get(url, headers=headers)
    data = res.json()[0]

    # Show the image
    st.image(data["url"], use_container_width=True)

    # Show breed info
    breed = data["breeds"][0]
    st.subheader(breed["name"])
    st.markdown(f"**Temperament:** {breed.get('temperament', 'Unknown')}")
    st.markdown(f"**Life span:** {breed.get('life_span', 'Unknown')}")
    st.markdown(f"**Breed group:** {breed.get('breed_group', 'Unknown')}")
    st.markdown(f"**Origin:** {breed.get('origin', 'Unknown')}")
else:
    st.info("Select a breed and click the button 🐶")
