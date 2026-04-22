import streamlit as st
import replicate
import os

# ==========================================
# 1. הגדרות האתר (עלינו ליגה!)
# ==========================================
st.set_page_config(page_title="Pro AI Video Studio", page_icon="🎬", layout="wide")
st.title("🎬 הסטודיו המקצועי - מנוע אחידות")

# חיבור מאובטח ל-Replicate
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("⚠️ מפתח API חסר ב-Secrets!")
    st.stop()

# ==========================================
# 2. תפריט צד: הגדרות במאי (Style Lock)
# ==========================================
with st.sidebar:
    st.header("⚙️ הגדרות במאי (סגנון קבוע)")
    st.markdown("הטקסט כאן יתווסף **אוטומטית** לכל סרטון כדי למנוע קפיצות גרפיות ושינויי רקע.")
    
    global_style = st.text_area(
        "סגנון הסרט (Style):", 
        value="Cinematic, 4k resolution, hyper-realistic, dark moody lighting, exact same background as the image",
        height=150
    )
    st.success("✅ נעילת סגנון מופעלת")

# ==========================================
# 3. מסך העבודה המרכזי
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. העלאת עוגן (תמונת מקור)")
    uploaded_image = st.file_uploader("בחר תמונה", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        st.image(uploaded_image, caption="הדמות והרקע ננעלו.")

with col2:
    st.subheader("2. פעולת הדמות בסצנה הנוכחית")
    action_prompt = st.text_area("מה קורה עכשיו?", placeholder="למשל: הדמות מסתכלת למצלמה ומחייכת קלות...")
    generate_btn = st.button("🚀 צור שוט מדוייק")

st.divider()

# ==========================================
# 4. מנוע יצירת הוידאו
# ==========================================
if generate_btn:
    if not uploaded_image or not action_prompt:
        st.error("חובה להעלות תמונה ולכתוב פעולה!")
    else:
        # ה"קסם": חיבור הפעולה שלך עם הסגנון הקבוע של הבמאי!
        final_prompt = f"{action_prompt}. {global_style}"
        
        st.info(f"🎥 **הפקודה המלאה שנשלחת למודל:** {final_prompt}")
        
        with st.spinner("⏳ מייצר שוט באחידות מלאה... (כ-2 דקות)"):
            try:
                # שמירה זמנית של התמונה
                with open("temp_image.jpg", "wb") as f:
                    f.write(uploaded_image.getbuffer())
                
                # הפעלת המודל
                output = replicate.run(
                    "minimax/video-01",
                    input={
                        "prompt": final_prompt,
                        "first_frame_image": open("temp_image.jpg", "rb")
                    }
                )
                
                st.success("✅ השוט נוצר בהצלחה ובסגנון אחיד!")
                
                # חילוץ הקישור לוידאו
                video_url = output[0] if isinstance(output, list) else output
                st.video(str(video_url))
                
            except Exception as e:
                st.error(f"שגיאה: {e}")
