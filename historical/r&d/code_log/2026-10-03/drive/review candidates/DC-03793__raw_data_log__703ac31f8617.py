import os
os.environ["CREMONA_DATABASE_PATH"] = os.path.expanduser("~/ecdata")


from sage.databases.cremona import CremonaDatabase
db = CremonaDatabase()


print("✅ Full Cremona database loaded successfully!")
print(f"   Total curves: {len(db):,}")
print(f"   Largest conductor: {db.largest_conductor()}")
print(f"   Example high-rank curve (rank 3): 5077a1 available? {'5077a1' in db}")
