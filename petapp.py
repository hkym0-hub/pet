import streamlit as st
import requests

st.set_page_config(page_title="🐾 Pet Search", layout="wide")

st.title("🐶 Pet Adoption Finder")
st.write("Find adoptable pets by animal type and location (using Petfinder API).")

# --- Get access token ---
@st.cache_data(ttl=3600)
def get_token():
    url = "https://api.petfinder.com/v2/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": st.secrets["api_keys"]["petfinder_key"],
        "client_secret": st.secrets["api_keys"]["petfinder_secret"]
    }
    return requests.post(url, data=data).json().get("access_token")

# --- Search pets ---
def search_pets(token, animal_type, location, limit=6):
    url = f"https://api.petfinder.com/v2/animals?type={animal_type}&location={location}&limit={limit}"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers).json().get("animals", [])

# --- UI ---
col1, col2 = st.columns(2)
animal_type = col1.selectbox("Animal Type", ["dog", "cat", "rabbit", "bird"])
location = col2.text_input("Location (ZIP or city)", "10001")

if st.button("🔍 Search"):
    token = get_token()
    pets = search_pets(token, animal_type, location)
    if not pets:
        st.warning("No pets found. Try another location.")
    else:
        for pet in pets:
            cols = st.columns([1, 2])
            if pet["photos"]:
                cols[0].image(pet["photos"][0]["medium"], use_container_width=True)
            else:
                cols[0].write("📷 No image")
            cols[1].markdown(f"### {pet['name']}")
            cols[1].markdown(f"**Age:** {pet['age']} | **Gender:** {pet['gender']}")
            desc = pet["description"] or "No description available."
            cols[1].write(desc[:300] + ("..." if len(desc) > 300 else ""))
            st.divider()
