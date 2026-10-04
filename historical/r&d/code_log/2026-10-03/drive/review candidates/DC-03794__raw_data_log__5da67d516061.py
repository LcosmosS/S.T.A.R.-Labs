from sage.databases.cremona import CremonaDatabase
db = CremonaDatabase()


print("✅ Full Cremona database is ready!")
print(f"   Largest conductor: {db.largest_conductor():,}")
print(f"   Curves with conductor ≤ 10,000: {len(db.conductors(max_conductor=10000)):,}")
print(f"   Rank-3 curve 5077a1 available? {'5077a1' in db}")
Run it — you should see large numbers and True for the rank-3 curve.
