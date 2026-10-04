from astroquery.vizier import Vizier

# Test query with a smaller radius
Vizier.ROW_LIMIT = 10000  # Small limit to test
result = Vizier(columns=['RAJ2000', 'DEJ2000']).query_region(
    "134.6125 +57.2325", radius="1d", catalog="II/349/ps1"
)
if len(result) == 0:
    print("No data returned.")
else:
    print(f"Returned {len(result[0])} rows.")