import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def log_chat(question: str, answer: str, visitor_name: str = None,
             visitor_email: str = None, ip_address: str = None,
             user_agent: str = None):
    try:
        supabase.table("chat_logs").insert({
            "question": question,
            "answer": answer,
            "visitor_name": visitor_name,
            "visitor_email": visitor_email,
            "ip_address": ip_address,
            "user_agent": user_agent,
        }).execute()
    except Exception as e:
        # Logging fail hone se chatbot ka response block nahi hona chahiye
        print(f"Failed to log chat: {e}")