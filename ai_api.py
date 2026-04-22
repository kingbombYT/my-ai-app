import requests

# המפתח שלך נשאר כאן, פשוט וקל
API_KEY = "91zxw8LmYvNbfMSXcKUFKGVGntEcN6zi"
API_URL = "https://api.mistral.ai/v1/chat/completions"

def chat_with_ai(prompt):
    """זו הפונקציה הרגילה שמדברת עם הבינה המלאכותית"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-tiny",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

def perform_action(command):
    """זה 'המוח' החדש שמנתח אם ביקשת פעולה מיוחדת או רק שיחה"""
    
    # פעולה 1: חיפוש (כרגע רק מדמה חיפוש)
    if "חפש" in command:
        query = command.replace("חפש", "").strip()
        return f"🔍 מפעיל כלי חיפוש... מחפש ברשת את: '{query}' (דמו - בהמשך נחבר את זה לגוגל)"
    
    # פעולה 2: יצירת דוח מקצועי אוטומטי (לפי שלב 5 בתוכנית שלך)
    elif "דוח" in command:
        topic = command.replace("דוח", "").strip()
        print(f"🛠️ מפעיל סוכן AI ליצירת דוח שוק על '{topic}'...")
        # אנחנו בונים ל-AI הנחיה מורכבת מאחורי הקלעים
        prompt = f"Write a short, professional market analysis report for '{topic}'. Include target audience, competitors, and growth potential. Format with bullet points."
        return chat_with_ai(prompt)
    
    # ברירת מחדל: אם אין פקודה מיוחדת, תתנהג כמו צ'אט רגיל
    else:
        return chat_with_ai(command)

# =============================================
# לולאת האפליקציה הראשית
# =============================================
print("🚀 המערכת מוכנה! הקלד 'quit' כדי לצאת.")
print("💡 נסה להקליד משהו רגיל, או לנסות את הפעולות החדשות:")
print("   - חפש מתכון לפנקייק")
print("   - דוח אפליקציות כושר\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["quit", "exit", "יציאה"]:
        print("להתראות!")
        break

    print("⏳ חושב/מבצע...")
    result = perform_action(user_input)
    print(f"AI: {result}\n")