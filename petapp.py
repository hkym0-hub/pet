import streamlit as st
import requests

st.title("🐾 Random Dog Viewer")

if st.button("Show me a dog!"):
    res = requests.get("https://dog.ceo/api/breeds/image/random")
    data = res.json()
    st.image(data["message"], caption="Here's a cute dog!", use_container_width=True)
else:
    st.info("Click the button to see a random dog 🐶")
