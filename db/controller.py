import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

db = create_client(
    supabase_key=os.environ.get("SUPABASE_KEY"),
    supabase_url=os.environ.get("SUPABASE_URL"),
)
