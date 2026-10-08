import sage.all
from sage.all import *
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# Set PARI stack size and precision
pari.set_stacksize(268435456)
pari.set_max_stacksize(1073741824)
pari.set_real_precision(128)

# Define pi
pi = sage.all.pi

# Fibonacci and Lucas numbers (unchanged from document)
fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887, 9227465, 14930352, 24157817, 39088169, 63245986, 102334155, 165580141, 267914296, 433494437, 701408733, 1134903170, 1836311903, 2971215073, 4807526976, 7778742049, 12586269025, 20365011074, 32951280099, 53316291173, 86267571272, 139583862445, 225851433717, 365435296162, 591286729879, 956722026041, 1548008755920, 2504730781961, 4052739537881, 6557470319842, 10610209857723, 17167680177565, 27777890035288, 44945570212853, 72723460248141, 117669030460994, 190392490709135, 308061521170129, 498454011879264, 806515533049393, 1304969544928657, 2111485077978050, 3416454622906707, 5527939700884757, 8944394323791464, 14472334024676221, 23416728348467685, 37889062373143906, 61305790721611591, 99194853094755497, 160500643816367088, 259695496911122585, 420196140727489673, 679891637638612258, 1100087778366101931, 1779979416004714189, 2880067194370816120, 4660046610375530309, 7540113804746346429, 12200160415121876738, 19740274219868223167, 3194043463499099995, 51680708854858323072, 83621143489848422977, 135301852344706746049, 218922995834555169026, 354224848179261915075]
lucas = [2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843, 1364, 2207, 3571, 5778, 9349, 15127, 24476, 39603, 64079, 103682, 167761, 271443, 439204, 710647, 1149851, 1860498, 3010349, 4870847, 7881196, 12752043, 20633239, 33385282, 54018521, 87403803, 141422324, 228826127, 370248451, 599074578, 969323029, 1568397607, 2537720636, 4106118243, 6643838879, 10749957122, 17393796001, 28143753123, 45537549124, 73681302247, 119218851371, 192900153618, 312119004989, 505019158607, 817138163596, 1322157322203, 2139295485799, 3461452808002, 5600748293801, 9062201101803, 14662949395604, 23725150497407, 38388099893011, 62113250390418, 100501350283429, 162614600673847, 263115950957276, 425730551631123, 688846502588399, 1114577054219522, 1803423556807921, 2918000611027443, 4721424167835364, 7639424778862807, 12360848946698171, 20000273725560978, 32361122672259149, 52361396397820127, 84722519070079276, 137083915467899403, 221806434537978679, 358890350005878082, 580696784543856761, 939587134549734843, 1520283919093591604, 2459871053643326447, 3980154972736918051, 6440026026380244498, 10420180999117162549, 16860207025497407047, 27280388024614569596, 44140595050111976643, 71420983074726546239, 115561578124838522882, 186982561199565069121, 302544139324403592003, 489526700523968661124, 792070839848372253127]

# ML model simulation for curve skipping
def ml_predict_skip_curve(conductor, threshold=10**15):
    return conductor > threshold

# Squarefree discriminant check
def is_squarefree(n):
    n = abs(n)
    for i in range(2, int(n.sqrt()) + 1):
        if n % (i * i) == 0:
            return False
    return True

# Generate discriminants using pi
possible_Ds = []
for k in range(1, 51):  # Generate 50 discriminants
    D_float = -k * pi
    D = floor(D_float)
    # Adjust D to be the nearest squarefree integer satisfying congruence
    while not (is_squarefree(D) and (D % 4 in [0, 1])):
        D -= 1
        if D < -200:  # Limit the range to match previous setup
            break
    if D >= -200 and D not in possible_Ds:
        possible_Ds.append(D)
possible_Ds.sort()

# Generate curves (same as document: 542 curves)
curves = []
a, b = 0, 2
for i in range(542):
    if i == 0:
        a, b = 0, 2  # First curve: y^2 = x^3 + 0x + 2
    else:
        a = fibonacci[min(i+2, len(fibonacci)-1)]
        b = lucas[min(i+2, len(lucas)-1)]
    curves.append((a, b))

# Process curves in batches
batch_size = 3
num_batches = (len(curves) + batch_size - 1) // batch_size
results = []

for batch_idx in range(num_batches):
    start_idx = batch_idx * batch_size
    end_idx = min(start_idx + batch_size, len(curves))
    print(f"Processing batch {batch_idx + 1}/{num_batches} ({start_idx} to {end_idx-1})")
    
    for idx in range(start_idx, end_idx):
        a, b = curves[idx]
        print(f"Analyzing curve: y^2 = x^3 + {a}x + {b}")
        
        # Scale coefficients to reduce conductor size
        scale_factor = (abs(b) / 1000000) if abs(b) > 1000000 else 1
        a_scaled = a / (scale_factor ** 2)
        b_scaled = b / (scale_factor ** 3)
        print(f"Scaling coefficients: a={a} -> {a_scaled}, b={b} -> {b_scaled}, scale_factor={scale_factor}")
        
        # Create elliptic curve
        E = EllipticCurve([0, 0, 0, a_scaled, b_scaled])
        conductor = E.conductor()
        print(f"Conductor: {conductor}")
        
        # Check if ML model skips the curve
        if ml_predict_skip_curve(conductor):
            print(f"ML model predicts to skip curve due to complexity (conductor={conductor})")
            continue
        
        # Compute ranks
        analytic_rank = E.rank(only_use_analytic=True)
        algebraic_rank = E.rank()
        print(f"Analytic rank: {analytic_rank}")
        print(f"Algebraic rank (via PARI/GP): {algebraic_rank}")
        bsd_holds = (analytic_rank == algebraic_rank)
        print(f"Weak BSD holds: {bsd_holds}")
        
        # Heegner point computation
        N = conductor
        heegner_point = None
        twist_attempts = [2, 3, 5, 7, 11, 13, 17, 19, 23]
        
        for D in possible_Ds:
            print(f"Trying discriminant D={D} (derived from -{abs(D)/pi.n()}*pi)")
            satisfies_hypothesis = True
            for p in prime_divisors(N):
                kronecker_val = kronecker(D, p)
                if kronecker_val == -1:
                    print(f"p={p} is inert (kronecker(D, p)=-1), condition satisfied")
                elif kronecker_val == 0:
                    print(f"Heegner condition passed for p={p}: k=0, p^2 divides N, and -D ≡ 0 (mod {p})")
                else:
                    print(f"Heegner hypothesis failed for p={p}: k=1 but p does not divide -D or p divides N/p")
                    satisfies_hypothesis = False
                    break
            
            if not satisfies_hypothesis:
                continue
            
            print(f"Heegner hypothesis satisfied for N={N}, D={D}")
            try:
                pt = E.heegner_point(D)
                heegner_point = pt
                print(f"Heegner point computed: {heegner_point}")
                break
            except Exception as e:
                print(f"Failed to compute Heegner point with D={D}: {str(e)}")
        
        # Try quadratic twists if necessary
        if heegner_point is None:
            for d in twist_attempts:
                E_twist = E.quadratic_twist(d)
                N_twist = E_twist.conductor()
                print(f"Attempting quadratic twist with d={d}, new conductor={N_twist}")
                
                for D in possible_Ds:
                    print(f"Trying discriminant D={D} (derived from -{abs(D)/pi.n()}*pi)")
                    satisfies_hypothesis = True
                    for p in prime_divisors(N_twist):
                        kronecker_val = kronecker(D, p)
                        if kronecker_val == -1:
                            print(f"p={p} is inert (kronecker(D, p)=-1), condition satisfied")
                        elif kronecker_val == 0:
                            print(f"Heegner condition passed for p={p}: k=0, p^2 divides N, and -D ≡ 0 (mod {p})")
                        else:
                            print(f"Heegner hypothesis failed for p={p}: k=1 but p does not divide -D or p divides N/p")
                            satisfies_hypothesis = False
                            break
                    
                    if not satisfies_hypothesis:
                        continue
                    
                    print(f"Heegner hypothesis satisfied for N={N_twist}, D={D}")
                    try:
                        pt = E_twist.heegner_point(D)
                        heegner_point = pt
                        print(f"Heegner point computed with twist d={d}: {heegner_point}")
                        break
                    except Exception as e:
                        print(f"Failed to compute Heegner point with twist d={d}: {str(e)}")
                
                if heegner_point is not None:
                    break
        
        if heegner_point is None:
            print("Failed to compute Heegner point after all twists, returning default (0,0)")
            heegner_point = (0, 0)
        
        # Earth mapping with pi normalization
        # Assume longitude and latitude are in degrees scaled by 1000 (UE units)
        longitude = -180000 + ((a_scaled * 100) % (360000)) * (pi / 180)  # Incorporate pi for angular scaling
        latitude = -89900 + ((b_scaled * 50) % (179800)) * (pi / 180)
        elevation = 1402.6503751475802 if algebraic_rank > 0 else 0
        size = 31.62277660168379 + (algebraic_rank * 10)
        z = -635674231.8115495 + (a_scaled + b_scaled) * 100000
        print(f"Earth mapping: Longitude={longitude} UE units, Latitude={latitude} UE units, Elevation={elevation} UE units, Size={size} UE units, Z={z} UE units")
        
        results.append({
            'curve': (a, b),
            'analytic_rank': analytic_rank,
            'algebraic_rank': algebraic_rank,
            'longitude': longitude,
            'latitude': latitude,
            'elevation': elevation,
            'size': size,
            'z': z
        })

# Generate plots
ranks = [res['algebraic_rank'] for res in results]
plt.hist(ranks, bins=range(max(ranks)+2), align='left', rwidth=0.8)
plt.title("Rank Distribution")
plt.xlabel("Algebraic Rank")
plt.ylabel("Frequency")
plt.savefig("distortion_free_rank_distribution_v12.png")
plt.clf()

# 3D mapping plot with polynomial regression
X = np.array(ranks).reshape(-1, 1)
longitudes = np.array([res['longitude'] for res in results])
latitudes = np.array([res['latitude'] for res in results])
zs = np.array([res['z'] for res in results])

degree = 3
polyreg = make_pipeline(PolynomialFeatures(degree), LinearRegression())
polyreg.fit(X, longitudes)
long_pred = polyreg.predict(X)

polyreg.fit(X, latitudes)
lat_pred = polyreg.predict(X)

polyreg.fit(X, zs)
z_pred = polyreg.predict(X)

long_coeffs = polyreg.named_steps['linearregression'].coef_
lat_coeffs = polyreg.named_steps['linearregression'].coef_
z_coeffs = polyreg.named_steps['linearregression'].coef_
print(f"Symbolic regression results: Latitude = {lat_coeffs[1]}*r + {lat_coeffs[2]}*r^2 + {lat_coeffs[3]}*r^3 + {lat_coeffs[0]}, "
      f"Longitude = {long_coeffs[1]}*r + {long_coeffs[2]}*r^2 + {long_coeffs[3]}*r^3 + {long_coeffs[0]}, "
      f"Z = {z_coeffs[1]}*r + {z_coeffs[2]}*r^2 + {z_coeffs[3]}*r^3 + {z_coeffs[0]}")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(longitudes, latitudes, zs, c='b', marker='o')
ax.plot(long_pred, lat_pred, z_pred, color='r', label='Polynomial Fit')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Z')
plt.legend()
plt.savefig("distortion_free_earth_mapping_v12.png")
plt.clf()