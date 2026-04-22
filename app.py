import streamlit as st
import time
import os
# ייבוא הספרייה של גוגל
from vertexai.generative_models import GenerativeModel, Part
import vertexai

# =============================================
# הגדרות חיבור (נשתמש ב-Secrets של Streamlit)
# =============================================
# כאן השרת יחפש את הפרטים של הפרויקט שלך בגוגל
PROJECT_ID = st.secrets.get("GCP_PROJECT_ID", "your-project-id")
LOCATION = "us-central1" # האזור שבו המודל של Veo פועל

vertexai.init(project=PROJECT_ID, location=LOCATION)

def generate_video_veo(image_file, prompt):
    """
    הפונקציה ששולחת את התמונה והטקסט ל-Veo 3.1
    """
    # קריאת התמונה שהעלית
    image_bytes = image_file.read()
    image_part = Part.from_data(data=image_bytes, mime_type="image/png")
    
    # הגדרת המודל (Veo 3.1)
    # הערה: השם המדויק של המודל ב-API עשוי להשתנות, ודא שיש לך הרשאה אליו
    model = GenerativeModel("veo-3-1-video-generation") 
    
    # יצירת הוידאו על בסיס התמונה (Image-to-Video)
    # זה השלב שבו הדמות נשמרת עקבית!
    response = model.generate_content([image_part, prompt])
    
    # כאן אנחנו מקבלים את הקישור לוידאו שנוצר
    return response.candidates[0].content.parts[0].video_metadata.uri

# =============================================
# ממשק המשתמש (UI)
# =============================================
st.set_page_config(page_title="Veo 3.1 Video Studio", page_icon="🎬", layout="wide")
st.title("🎬 סטודיו Veo 3.1 אישי")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. העלאת דמות (Identity Anchor)")
    uploaded_image = st.file_uploader("העלה תמונה של הדמות שלך", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        st.image(uploaded_image, caption="הדמות שתהיה עקבית בוידאו")

with col2:
    st.subheader("2. פקודת בימוי")
    scene_prompt = st.text_area("מה הדמות עושה?", placeholder="למשל: הדמות מחייכת ומנופפת לשלום...")
    generate_btn = st.button("🚀 צור וידאו עם Veo 3.1")

st.divider()

if generate_btn:
    if not uploaded_image or not scene_prompt:
        st.error("חובה להעלות תמונה ולהוסיף תיאור!")
    else:
        with st.spinner("⏳ Veo 3.1 מעבד את הסצנה... שומר על עקביות הדמות..."):
            try:
                # כאן קורה החיבור האמיתי!
                video_url = generate_video_veo(uploaded_image, scene_prompt)
                
                st.success("✅ הוידאו נוצר!")
                st.video(video_url)
            except Exception as e:
                # אם עדיין אין לך הרשאות API, זה יציג שגיאה מסודרת
                st.error(f"שגיאת חיבור ל-API: {e}")
                st.info("טיפ: וודא שהגדרת את ה-Project ID ב-Secrets של Streamlit.")
