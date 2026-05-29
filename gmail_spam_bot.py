import os.path
import time
import joblib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://mail.google.com/']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def main():
    print("🧠 Loading AI Model...")
    model = joblib.load('spam_classifier_model.pkl')
    vectorizer = joblib.load('text_vectorizer.pkl')

    print("🔌 Connecting to Google...")
    service = authenticate_gmail()
    
    # Create a "memory bank" to store the IDs of emails we've already checked
    processed_emails = set()

    print("🎧 Bot is now actively listening for NEW emails. (Press Ctrl+C to stop)\n")

    # The Infinite Loop
    while True:
        try:
            # Ask Google for UNREAD emails
            results = service.users().messages().list(userId='me', q="is:unread in:inbox").execute()
            messages = results.get('messages', [])

            for msg in messages:
                msg_id = msg['id']

                # If the email ID is in our memory bank, skip it entirely!
                if msg_id in processed_emails:
                    continue
                
                # --- NEW EMAIL DETECTED ---
                full_msg = service.users().messages().get(userId='me', id=msg_id).execute()
                email_text = full_msg.get('snippet', '')
                
                text_matrix = vectorizer.transform([email_text])
                spam_prob = model.predict_proba(text_matrix)[0, 1]

                print(f"📥 New Email Caught: '{email_text[:50]}...'")
                
                if spam_prob >= 0.79:
                    print(f"🚨 SPAM DETECTED! (Confidence: {spam_prob*100:.1f}%) -> Moving to Spam.\n")
                    service.users().messages().modify(
                        userId='me', 
                        id=msg_id, 
                        body={'removeLabelIds': ['INBOX'], 'addLabelIds': ['SPAM']}
                    ).execute()
                else:
                    print(f"✅ Safe Email. (Confidence: {spam_prob*100:.1f}%) -> Ignored.\n")

                # Add this email's ID to the memory bank so we never process it again
                processed_emails.add(msg_id)

            # Pause the script for 15 seconds before asking Google again
            # This prevents Google from blocking you for making too many requests!
            time.sleep(15)

        except Exception as e:
            # If your internet cuts out for a second, this stops the bot from crashing
            print(f"⚠️ Network glitch: {e}. Retrying in 15 seconds...")
            time.sleep(15)

if __name__ == '__main__':
    main()