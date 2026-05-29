import streamlit as st
import joblib

# 1.Set up website
st.set_page_config(page_title="Spam Detector", page_icon="🕵️‍♂️")
st.title("AI Spam & Scam Detector 🕵️‍♂️")
st.write("Paste any suspicious text message, email, or DM below to see if it is safe.")

# 2.Load trained models
@st.cache_resource
def load_ai():
    model = joblib.load('spam_classifier_model.pkl')
    vectorizer = joblib.load('text_vectorizer.pkl')
    return model, vectorizer

model, vectorizer = load_ai()

# 3.Create User Interface
user_input = st.text_area("Message Content:", height=150, placeholder="Paste the message here...")

# 4.The Action(CLICK) Button
if st.button("Analyze Message"):
    if user_input.strip() == "":
        st.warning("Please paste some text first!")
    else:
        #Translate txt to math and predict
        text_matrix = vectorizer.transform([user_input])
        spam_prob = model.predict_proba(text_matrix)[0, 1]
        
        #Display results
        st.divider()
        if spam_prob >= 0.79:
            st.error(f"🚨 **WARNING: SPAM DETECTED!**")
            st.write(f"The AI is **{spam_prob*100:.1f}%** confident this is a scam or spam message.")
        else:
            st.success(f"✅ **LOOKS SAFE.**")
            st.write(f"The AI is **{(1-spam_prob)*100:.1f}%** confident this is a normal, legitimate message.")