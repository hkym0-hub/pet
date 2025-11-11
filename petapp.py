import streamlit as st
import requests
import random

st.title("🐾 The Dog API Explorer")

# ===========================
# ✅ Sidebar
# ===========================
st.sidebar.header("🔧 Settings")

# 1. API Key input
api_key = st.sidebar.text_input("Enter your Dog API key:", type="password")
if not api_key:
    st.sidebar.warning("🔑 Please enter your Dog API key to continue.")
    st.stop()

headers = {"x-api-key": api_key.strip()}

# 2. Breed selection / input
st.sidebar.markdown("### 🐶 Breed Info Settings")
selected_breed = st.sidebar.selectbox("Choose a breed:", ["-- Select --"])
input_breed = st.sidebar.text_input("Or type a breed name manually:")

# 3. AI Match settings
st.sidebar.markdown("### 🤖 AI Match Settings")
activity = st.sidebar.select_slider("How active are you?", ["Low", "Medium", "High"])
space = st.sidebar.radio("Home type:", ["Apartment", "House with yard"])
size_pref = st.sidebar.radio("Preferred dog size?", ["Small", "Medium", "Large"])
personality = st.sidebar.selectbox(
    "Describe your personality:", ["Calm", "Active", "Loyal", "Playful", "Independent", "Social"]
)

# 4. Dog Name Generator settings
st.sidebar.markdown("### 💬 Dog Name Generator")
name_style = st.sidebar.selectbox("Name vibe:", ["Cute", "Funny", "Cool", "Elegant"])
gender = st.sidebar.radio("Gender:", ["Male", "Female", "Neutral"])

# ===========================
# ✅ Get breed info
# ===========================
@st.cache_data
def get_breeds():
    res = requests.get("https://api.thedogapi.com/v1/breeds", headers=headers)
    return res.json()

breeds = get_breeds()
breed_names = [b["name"] for b in breeds]

# ===========================
# 🐶 TAB 1: Breed Info
# ===========================
tab1, tab2, tab3 = st.tabs(["🐶 Breed Info", "🤖 AI Match", "💬 Name Generator"])

with tab1:
    st.markdown("### 🔍 Breed Information")
    
    # Determine final breed
    final_breed = input_breed.strip() if input_breed.strip() else (
        selected_breed if selected_breed != "-- Select --" else None
    )
    
    if st.button("Show me this dog!"):
        if not final_breed:
            st.warning("Please select or type a breed name first 🐶")
        else:
            match = [b for b in breeds if final_breed.lower() in b["name"].lower()]
            if not match:
                st.error(f"❌ Could not find any breed matching '{final_breed}'.")
            else:
                breed = match[0]
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

                temperament = breed.get("temperament", "unique personality")
                first_trait = temperament.split(",")[0] if "," in temperament else temperament
                st.info(f"💡 The **{breed['name']}** is known for being {first_trait.lower().strip()} — a great companion!")

# ===========================
# 🤖 TAB 2: AI Match
# ===========================
with tab2:
    st.markdown("### 🤖 Find Your Perfect Dog Match")
    if st.button("Find My Match 💞"):
        candidates = []
        # Match by activity
        if activity == "Low":
            candidates = [b for b in breeds if "calm" in str(b.get("temperament", "")).lower()]
        elif activity == "High":
            candidates = [b for b in breeds if "energetic" in str(b.get("temperament", "")).lower()]
        else:
            candidates = [b for b in breeds if "friendly" in str(b.get("temperament", "")).lower()]
        
        # Size filter
        if size_pref == "Small":
            candidates = [b for b in candidates if "10" in b.get("weight", {}).get("imperial", "")]
        elif size_pref == "Large":
            candidates = [b for b in candidates if "70" in b.get("weight", {}).get("imperial", "")]
        
        # Match by personality keyword
        candidates = [b for b in candidates if personality.lower() in str(b.get("temperament", "")).lower()] or candidates

        match_breed = random.choice(candidates) if candidates else random.choice(breeds)
        
        st.subheader(f"💖 Your Match: {match_breed['name']}")
        st.markdown(f"**Temperament:** {match_breed.get('temperament', 'Unknown')}")
        st.markdown(f"**Life span:** {match_breed.get('life_span', 'Unknown')}")
        img = requests.get(f"https://api.thedogapi.com/v1/images/search?breed_id={match_breed['id']}", headers=headers).json()[0]
        st.image(img["url"], use_container_width=True)
        st.info(f"✨ Because you’re **{personality.lower()}**, the **{match_breed['name']}** shares your {personality.lower()} spirit!")

# ===========================
# 💬 TAB 3: Dog Name Generator
# ===========================
with tab3:
    st.markdown("### 💬 Dog Name Generator")
    if st.button("Generate Name ✨"):
        cute_names = ["Coco", "Milo", "Lulu", "Pong", "Toto"]
        funny_names = ["Barky", "Sir Waggington", "Noodle", "Biscuit"]
        cool_names = ["Rex", "Shadow", "Blaze", "Hunter"]
        elegant_names = ["Bella", "Duchess", "Chanel", "Aria"]

        pool = {"Cute": cute_names, "Funny": funny_names, "Cool": cool_names, "Elegant": elegant_names}[name_style]

        if gender == "Male":
            pool = [n for n in pool if not n.endswith("a")]
        elif gender == "Female":
            pool = [n for n in pool if n.endswith("a") or n in ["Lulu", "Bella", "Aria"]]

        name = random.choice(pool)
        st.success(f"✨ How about **{name}**?")
        descriptions = {
            "Coco": "Sweet and classic, perfect for a gentle dog.",
            "Rex": "Strong and bold — ideal for an adventurous dog.",
            "Lulu": "Playful and affectionate, fits a small energetic pup.",
            "Sir Waggington": "For a noble dog with endless charm.",
            "Aria": "Graceful and calm, perfect for an elegant friend.",
        }
        if name in descriptions:
            st.caption(descriptions[name])
