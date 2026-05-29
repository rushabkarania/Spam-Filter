from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
import joblib

# 1. Initialize the Web Server
app = FastAPI()

# 2. Loads the trained models
model = joblib.load('spam_classifier_model.pkl')
vectorizer = joblib.load('text_vectorizer.pkl')

# 3. Create the endpoint that Twilio will talk to
@app.post("/whatsapp")
async def reply_whatsapp(Body: str = Form(...)):
    """
    Twilio sends the incoming message to this function. 
    'Body' contains the actual text the user typed on their phone.
    """
    
    # Convert the incoming text into math
    text_matrix = vectorizer.transform([Body])
    
    # Compute the spam probability
    spam_prob = model.predict_proba(text_matrix)[0, 1]
    
    # Custom 0.79 threshold
    if spam_prob >= 0.79:
        reply_text = f"🚨 WARNING: This message looks like SPAM/SCAM. (Confidence: {spam_prob*100:.1f}%)"
    else:
        reply_text = f"✅ This message looks SAFE. (Spam Probability: {spam_prob*100:.1f}%)"

    
    # Use Twilio's specific XML format (TwiML) to text back
    twiml_response = MessagingResponse()
    twiml_response.message(reply_text)

    # Send the XML back to Twilio so it can route it to WhatsApp
    return Response(content=str(twiml_response), media_type="application/xml")