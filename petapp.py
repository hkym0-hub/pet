import streamlit as st
import requests
import random

st.title("🐾 The Dog API Explorer + AI Dog Match")

# ✅ 1. API Key
api_key = st.secrets["api_keys"].get("dogapi", None)

if api_key:
    st.success("✅ API key loaded successfully! Authentication confirmed.")
else:
    st.error("❌ API key not found. Please check your Streamlit secrets settings.")
    st.stop()

headers = {"x-api-key": api_key}

# ✅ 2. Fetch breeds
@st.cache_data
def get_breeds():
    res = requests.get("https://api.thedogapi.com/v1/breeds", headers=headers)
    return res.json()

breeds = get_breeds()
breed_names = [b["name"] for b in breeds]

# ✅ 3. Breed selection
st.subheader("🐶 Choose or Enter a Breed")
col1, col2 = st.columns(2)
with col1:
    selected_breed = st.selectbox("Select from the list:", ["(Choose one)"] + breed_names)
with col2:
    manual_breed = st.text_input("...or type a breed name manually:")

final_breed = manual_breed if manual_breed else selected_breed

# ✅ 4. Breed info
if st.button("Show me this dog!"):
    try:
        breed = next(b for b in breeds if b["name"].lower() == final_breed.lower())
        breed_id = breed["id"]

        url = f"https://api.thedogapi.com/v1/images/search?breed_id={breed_id}"
        res = requests.get(url, headers=headers)
        data = res.json()[0]

        st.image(data["url"], use_container_width=True)
        st.subheader(breed["name"])
        st.markdown(f"**Temperament:** {breed.get('temperament', 'Unknown')}")
        st.markdown(f"**Life span:** {breed.get('life_span', 'Unknown')}")
        st.markdown(f"**Breed group:** {breed.get('breed_group', 'Unknown')}")
        st.markdown(f"**Origin:** {breed.get('origin', 'Unknown')}")

        # ✨ Short personality description
        temperament = breed.get("temperament", "unique personality")
        first_trait = temperament.split(",")[0] if "," in temperament else temperament
        st.info(f"💡 {breed['name']} dogs are known for being {first_trait.lower().strip()} — a perfect choice if you love that kind of vibe!")

    except StopIteration:
        st.warning("⚠️ That breed name was not found. Please check spelling or pick from the list.")
else:
    st.info("Select or type a breed and click the button 🐶")

# ─────────────────────────────────────────────
# 💬 Dog Name Generator
# ─────────────────────────────────────────────
st.markdown("---")
st.header("💬 Dog Name Generator")

vibe = st.selectbox("What kind of vibe do you want for the name?", ["Funny", "Cute", "Cool"])
gender = st.radio("Gender:", ["Male", "Female", "Neutral"])

names = {
    "Funny": {
        "Male": ["Bark Twain", "Chew Bacca", "Sir Waggington"],
        "Female": ["Mary Puppins", "Furrgie", "Chewberta"],
        "Neutral": ["Dogtor Strange", "Paw-casso", "Woofles"],
    },
    "Cute": {
        "Male": ["Teddy", "Coco", "Mochi"],
        "Female": ["Luna", "Bella", "Daisy"],
        "Neutral": ["Peach", "Puppy", "Snow"],
    },
    "Cool": {
        "Male": ["Rex", "Ace", "Shadow"],
        "Female": ["Nova", "Raven", "Storm"],
        "Neutral": ["Blaze", "Echo", "Onyx"],
    },
}

descriptions = {
    "Bark Twain": "A literary genius with a loud bark and a big heart.",
    "Chew Bacca": "Perfect for a furry sidekick with Wookiee energy.",
    "Sir Waggington": "Distinguished, loyal, and always wagging in style.",
    "Mary Puppins": "Practically perfect in every way — especially for small, charming dogs.",
    "Dogtor Strange": "Mysterious, clever, and full of magical energy.",
    "Rex": "Strong and confident, fit for a brave guardian.",
    "Luna": "A gentle soul who shines like the moon.",
    "Mochi": "Sweet, soft, and irresistibly adorable.",
}

if st.button("Generate Dog Name"):
    pool = names.get(vibe, {}).get(gender, [])
    if not pool:
        pool = names["Funny"]["Neutral"]
    name = random.choice(pool)
    st.success(f"✨ How about **{name}**?")
    if name in descriptions:
        st.caption(descriptions[name])

# ─────────────────────────────────────────────
# 🤖 AI Dog Match
# ─────────────────────────────────────────────
st.markdown("---")
st.header("🤖 AI Dog Match: Find Your Perfect Pup!")

user_trait = st.selectbox(
    "Describe your personality:",
    ["Calm", "Active", "Loyal", "Playful", "Independent", "Social"]
)

if st.button("Find My Match!"):
    matches = []

    # Simple temperament keyword matching
    for breed in breeds:
        temperament = breed.get("temperament", "").lower()
        if user_trait.lower() in temperament:
            matches.append(breed)

    if matches:
        match = random.choice(matches)
        st.image(f"https://cdn2.thedogapi.com/images/{match['reference_image_id']}.jpg", width=400)
        st.subheader(f"Your match: 🐶 {match['name']}")
        st.markdown(f"**Temperament:** {match.get('temperament', 'Unknown')}")
        st.markdown(f"**Life span:** {match.get('life_span', 'Unknown')}")

        # Friendly AI-style explanation
        st.info(f"✨ Because you’re **{user_trait.lower()}**, the **{match['name']}** suits you perfectly — "
                f"they share your {user_trait.lower()} spirit and will easily adapt to your personality!")

    else:
        st.warning("Sorry, no perfect match found — try another trait 🐾")
