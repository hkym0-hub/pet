import streamlit as st
import requests

st.title("🐾 Random Animal Viewer")

# Dictionary of supported animals and their APIs
animal_apis = {
    "Dog": "https://dog.ceo/api/breeds/image/random",
    "Cat": "https://api.thecatapi.com/v1/images/search",
    "Fox": "https://randomfox.ca/floof/",
    "Duck": "https://random-d.uk/api/v2/random"
}

# Select the animal
animal = st.selectbox("Choose an animal:", list(animal_apis.keys()))

if st.button("Show me the animal!"):
    api_url = animal_apis[animal]
    res = requests.get(api_url)
    data = res.json()

    # Extract image URL based on the API’s format
    if animal == "Dog":
        img_url = data["message"]
    elif animal == "Cat":
        img_url = data[0]["url"]
    elif animal == "Fox":
        img_url = data["image"]
    elif animal == "Duck":
        img_url = data["url"]

    st.image(img_url, caption=f"Here's a cute {animal.lower()}!", use_container_width=True)
else:
    st.info("Pick an animal and click the button 🐶🐱🦊🦆")
