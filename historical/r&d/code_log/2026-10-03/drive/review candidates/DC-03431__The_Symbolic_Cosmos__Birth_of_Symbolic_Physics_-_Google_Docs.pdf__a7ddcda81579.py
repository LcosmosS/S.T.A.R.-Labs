sha_order = (leading_coeff * tors_order**2) / (omega * reg * tamagawa)
print(f"Adjusted |Sha(E)| to match: {sha_order}")
except Exception as e:
print(f"Failed to compute BSD invariants: {e}")
return False, None
log_delta = math.log(abs(delta)) if delta != 0 else 0
log_cond = math.log(conductor) if conductor > 0 else 0
features = [a, b, log_delta, log_cond, tors_order]
print("-" * 20)
return success, features
# Initialize data for classifier
X_data = []
y_data = []
classifier = None
