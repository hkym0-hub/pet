import streamlit as st
import requests
import random

st.title("🐾 The Dog API Explorer")

# ✅ 1. API 키 불러오기
api_key = st.secrets["api_keys"].get("dogapi", None)

# ✅ 2. API 키 검증
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

# ✅ 4. 품종 선택 또는 직접 입력
st.subheader("🐶 Choose or Enter a Breed")
col1, col2 = st.columns(2)
with col1:
    selected_breed = st.selectbox("Select from the list:", ["(Choose one)"] + breed_names)
with col2:
    manual_breed = st.text_input("...or type a breed name manually:")

# 최종 선택
final_breed = manual_breed if manual_breed else selected_breed

# ✅ 5. 버튼 클릭 시 이미지 + 정보 표시
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

        # 🌟 추가: 짧은 설명글
        st.info(f"💡 {breed['name']} dogs are known for their {breed.get('temperament', 'unique personality').split(',')[0].lower()} nature!")

    except StopIteration:
        st.warning("⚠️ That breed name was not found. Please check spelling or pick from the list.")

else:
    st.info("Select or type a breed and click the button 🐶")

# ─────────────────────────────────────────────
# 💬 추가 섹션: Dog Name Generator
# ─────────────────────────────────────────────
st.markdown("---")
st.header("💬 Dog Name Generator")

vibe = st.selectbox("What kind of vibe do you want for the name?", ["Funny", "Cute", "Cool"])
gender = st.radio("Gender:", ["Male", "Female", "Neutral"])

# 이름 후보 리스트
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

# 간단한 설명도 함께
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

# 버튼 클릭 시 이름 추천
if st.button("Generate Dog Name"):
    pool = names.get(vibe, {}).get(gender, [])
    if not pool:  # 빈 리스트일 경우 대비
        pool = names["Funny"]["Neutral"]

    name = random.choice(pool)
    st.success(f"✨ How about **{name}**?")
    if name in descriptions:
        st.caption(descriptions[name])
