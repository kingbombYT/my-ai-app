import streamlit as st
import replicate
import os

# הגדרות האתר
st.set_page_config(page_title="AI Video Studio", page_icon="🎬", layout="wide")
st.title("🎬 הסטודיו האישי שלי - Image to Video")

# חיבור למפתח ששמת ב-Secrets
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("⚠️ מפתח API חסר ב-Secrets!")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. העלאת דמות (עוגן)")
    uploaded_image = st.file_uploader("בחר תמונה", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        st.image(uploaded_image)

with col2:
    st.subheader("2. מה קורה בסצנה?")
    prompt = st.text_area("תיאור:", placeholder="למשל: הדמות רוקדת בגשם...")
    generate_btn = st.button("🚀 צור וידאו")

if generate_btn:
    if not uploaded_image or not prompt:
        st.error("חובה תמונה ותיאור!")
    else:
        with st.spinner("⏳ המודל עובד... זה לוקח כ-2 דקות..."):
            try:
                # שמירה זמנית של התמונה
                with open("temp_image.jpg", "wb") as f:
                    f.write(uploaded_image.getbuffer())
                
                # הפעלת המודל
                output = replicate.run(
                    "minimax/video-01",
                    input={
                        "prompt": prompt,
                        "first_frame_image": open("temp_image.jpg", "rb")
                    }
                )
                st.success("מוכן!")
                st.video(output)
            except Exception as e:
                st.error(f"שגיאה: {e}")
