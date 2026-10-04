# Test query in a different region
Vizier.ROW_LIMIT = -1
result = Vizier(columns=['+RAJ2000', '+DEJ2000']).query_region(
    "194.95 +27.98", radius="0.1d", catalog="II/349"
)
if len(result) == 0:
    print("No data returned for Coma Cluster region.")
else:
    print(f"Returned {len(result[0])} rows for Coma Cluster region (0.1° radius).")