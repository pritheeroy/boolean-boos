from supabase import create_client, Client

url: str = "https://ytjttwkyfkltqqxpdaox.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl0anR0d2t5ZmtsdHFxeHBkYW94Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDA1MzA2NDQsImV4cCI6MjAxNjEwNjY0NH0.BJxaaSqeCJDp2vKOMj2UNW5YwytqezaLfez24kPMuZs"

supabase: Client = create_client(url, key)

data = supabase.table("temp_products").select("*").execute()
rows = data.data

print(rows)