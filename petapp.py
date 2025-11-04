import streamlit as st
import requests

st.title("🐶 The Dog API Viewer")

api_key = st.secrets["api_keys"]["dogapi"]

headers = {"x-api-key": api_key}

if st.button("Show me a dog!"):
    res = requests.get("https://api.thedogapi.com/v1/images/search", headers=headers)
    data = res.json()
    st.image(data[0]["url"], caption="Here's a cute dog!", use_container_width=True)
else:
    st.info("Click the button to fetch a dog image 🐾")
