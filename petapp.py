import streamlit as st
import requests

st.title("🐾 The Dog API Explorer")

# ✅ 1. API 키 불러오기
api_key = st.secrets["api_keys"].get("dogapi", None)

# ✅ 2. API 키 검증 메시지
if api_key:
    st.success("✅ API key loaded successfully! Authentication confirmed.")
else:
    st.error("❌ API key not found. Please check your Streamlit secrets settings.")
    st.stop()  # 키 없으면 아래 코드 실행 중단

headers = {"x-api-key": api_key}

# ✅ 3. 품종 정보 불러오기 (캐싱)
@st.cache_data
def get_breeds():
    res = requests.get("https://api.thedogapi.com/v1/breeds", headers=headers)
    return res.json()

breeds = get_breeds()
breed_names = [b["name"] for b in breeds]

# ✅ 4. 품종 선택
selected_breed = st.selectbox("Choose a breed:", breed_names)

# ✅ 5. 버튼 클릭 시 이미지 + 정보 출력
if st.button("Show me this dog!"):
    # 품종 ID 찾기
    breed_id = next(b["id"] for b in breeds if b["name"] == selected_breed)

    # 해당 품종 이미지 요청
    url = f"https://api.thedogapi.com/v1/images/search?breed_id={breed_id}"
    res = requests.get(url, headers=headers)
    data = res.json()[0]

    # 이미지 표시
    st.image(data["url"], use_container_width=True)

    # 품종 정보 표시
    breed = data["breeds"][0]
    st.subheader(breed["name"])
    st.markdown(f"**Temperament:** {breed.get('temperament', 'Unknown')}")
    st.markdown(f"**Life span:** {breed.get('life_span', 'Unknown')}")
    st.markdown(f"**Breed group:** {breed.get('breed_group', 'Unknown')}")
    st.markdown(f"**Origin:** {breed.get('origin', 'Unknown')}")
else:
    st.info("Select a breed and click the button 🐶")
