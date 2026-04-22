import requests
import streamlit as st

# הגדרות ה-API שלנו
API_KEY = st.secrets["MISTRAL_API_KEY"]
API_URL = "https://api.mistral.ai/v1/chat/completions"

def chat_with_ai(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-tiny",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ שגיאה: {response.text}"

def perform_action(command):
    # הפונקציות החכמות שלנו
    if "חפש" in command:
        query = command.replace("חפש", "").strip()
        return f"🔍 מפעיל כלי חיפוש... מחפש ברשת את: '{query}' (דמו)"
    
    elif "דוח" in command:
        topic = command.replace("דוח", "").strip()
        prompt = f"Write a short, professional market analysis report for '{topic}'. Include target audience, competitors, and growth potential. Format with bullet points."
        return chat_with_ai(prompt)
    
    return None # אם זו סתם שיחה, נחזיר 'כלום' כדי שהאתר ידע שזה צ'אט רגיל

# =============================================
# עיצוב האתר (Streamlit UI)
# =============================================
st.set_page_config(page_title="ה-AI שלי", page_icon="🤖")
st.title("🤖 הסוכן החכם שלי")

# הגדרה ששומרת את היסטוריית השיחה על המסך
if "messages" not in st.session_state:
    st.session_state.messages = []

# הצגת כל ההודעות הקודמות בצ'אט
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# שורת ההקלדה למטה
if prompt := st.chat_input("הקלד משהו, או נסה 'דוח' / 'חפש'"):
    
    # הצגת מה שאתה כתבת
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # הבוט חושב ועונה
    with st.chat_message("assistant"):
        action_result = perform_action(prompt)
        
        # בודק אם הפעלנו פעולה או שזו שיחה רגילה
        if action_result:
            response = action_result
        else:
            response = chat_with_ai(prompt)
            
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
