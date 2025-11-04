import streamlit as st
import requests
import random

st.title("🐾 The Dog API Explorer")

# ✅ 1. API 키 불러오기
api_key = st.secrets["api_keys"].get("dogapi", None)

# ✅ 2. API 키 검증 메시지
if api_key:
    st.success("✅ API key loaded successfully! Authentication confirmed.")
else:
    st.error("❌ API key not found. Please check your Streamlit secrets settings.")
    st.stop()

headers = {"x-api-key": api_key}

# ✅ 3. 품종 정보 불러오기 (캐싱)
@st.cache_data
def get_breeds():
    res = requests.get("https://api.thedogapi.com/v1/breeds", headers=headers)
    return res.json()

breeds = get_breeds()
breed_names = [b["name"] for b in breeds]

# --- 탭 UI ---
tab1, tab2, tab3 = st.tabs(["🐶 Breed Info", "🤖 AI Match", "💬 Name Generator"])

# ============================================================
# 🐶 TAB 1: Breed Info
# ============================================================
with tab1:
    st.markdown("### 🔍 Choose or type a breed name")
    col1, col2 = st.columns(2)

    with col1:
        selected_breed = st.selectbox("Choose a breed:", ["-- Select --"] + breed_names)
    with col2:
        input_breed = st.text_input("Or type a breed name manually:")

    final_breed = input_breed.strip() if input_breed.strip() else (
        selected_breed if selected_breed != "-- Select --" else None
    )

    if st.button("Show me this dog!"):
        if not final_breed:
            st.warning("Please select or type a breed name first 🐶")
        else:
            match = [b for b in breeds if final_breed.lower() in b["name"].lower()]
            if not match:
                st.error(f"❌ Could not find any breed matching '{final_breed}'. Please check spelling.")
            else:
                breed = match[0]
                breed_id = breed["id"]
                url = f"https://api.thedogapi.com/v1/images/search?breed_id={breed_id}"
                res = requests.get(url, headers=headers)
                data = res.json()[0]

                # 이미지 표시
                st.image(data["url"], use_container_width=True)
                st.subheader(breed["name"])
                st.markdown(f"**Temperament:** {breed.get('temperament', 'Unknown')}")
                st.markdown(f"**Life span:** {breed.get('life_span', 'Unknown')}")
                st.markdown(f"**Breed group:** {breed.get('breed_group', 'Unknown')}")
                st.markdown(f"**Origin:** {breed.get('origin', 'Unknown')}")

# ============================================================
# 🤖 TAB 2: AI 매칭 기능
# ============================================================
with tab2:
    st.markdown("### 🤖 Find Your Perfect Dog Match")

    # 사용자 정보 입력
    st.write("Answer a few questions to find your ideal dog breed:")
    activity = st.select_slider("How active are you?", ["Low", "Medium", "High"])
    space = st.radio("What kind of home do you live in?", ["Apartment", "House with yard"])
    size_pref = st.radio("Preferred dog size?", ["Small", "Medium", "Large"])

    if st.button("Find My Match 💞"):
        if activity == "Low":
            match_candidates = [b for b in breeds if "calm" in str(b.get("temperament", "")).lower()]
        elif activity == "High":
            match_candidates = [b for b in breeds if "energetic" in str(b.get("temperament", "")).lower()]
        else:
            match_candidates = [b for b in breeds if "friendly" in str(b.get("temperament", "")).lower()]

        if size_pref == "Small":
            match_candidates = [b for b in match_candidates if "Small" in b.get("weight", {}).get("imperial", "")]
        elif size_pref == "Large":
            match_candidates = [b for b in match_candidates if "70" in b.get("weight", {}).get("imperial", "")]

        if not match_candidates:
            st.warning("No perfect match found... showing a random cute dog instead 🐕")
            match_breed = random.choice(breeds)
        else:
            match_breed = random.choice(match_candidates)

        st.subheader(f"💖 Your Match: {match_breed['name']}")
        st.markdown(f"**Temperament:** {match_breed.get('temperament', 'Unknown')}")
        st.markdown(f"**Life span:** {match_breed.get('life_span', 'Unknown')}")

        img = requests.get(f"https://api.thedogapi.com/v1/images/search?breed_id={match_breed['id']}", headers=headers).json()[0]
        st.image(img["url"], use_container_width=True)

# ============================================================
# 💬 TAB 3: 강아지 이름 추천기
# ============================================================
with tab3:
    st.markdown("### 💬 Dog Name Generator")

    name_style = st.selectbox("What kind of vibe do you want for the name?", ["Cute", "Funny", "Cool", "Elegant"])
    gender = st.radio("Gender:", ["Male", "Female", "Neutral"])

    if st.button("Generate Name ✨"):
        cute_names = ["Coco", "Milo", "Lulu", "Pong", "Toto"]
        funny_names = ["Barky", "Sir Waggington", "Noodle", "Biscuit"]
        cool_names = ["Rex", "Shadow", "Blaze", "Hunter"]
        elegant_names = ["Bella", "Duchess", "Chanel", "Aria"]

        if name_style == "Cute":
            pool = cute_names
        elif name_style == "Funny":
            pool = funny_names
        elif name_style == "Cool":
            pool = cool_names
        else:
            pool = elegant_names

        # 성별 기반 약간의 필터
        if gender == "Male":
            pool = [n for n in pool if not n.endswith("a")]
        elif gender == "Female":
            pool = [n for n in pool if n.endswith("a") or n in ["Lulu", "Bella", "Aria"]]

        st.success(f"✨ How about **{random.choice(pool)}**?")
