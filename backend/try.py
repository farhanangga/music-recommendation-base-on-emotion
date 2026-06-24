from supabase_client import supabase

def test_connection():
    try:
        print("🔄 Testing Supabase connection...")

        res = supabase.table("music").select("*").limit(5).execute()

        print("✅ SUCCESS CONNECTED TO SUPABASE")

        print("\n📦 SAMPLE DATA:")
        for row in res.data:
            print(row)

        print("\nTOTAL ROWS:", len(res.data))

    except Exception as e:
        print("❌ ERROR CONNECTING TO SUPABASE")
        print(str(e))


if __name__ == "__main__":
    test_connection()