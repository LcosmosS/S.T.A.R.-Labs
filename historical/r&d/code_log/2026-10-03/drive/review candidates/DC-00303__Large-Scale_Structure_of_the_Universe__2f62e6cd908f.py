from numpy.polynomial.polynomial import Polynomial


# Define your data (X, Y are features)
X = df1[['ra', 'dec', 'redshift']]  # Example features
Y = df1['SFR']  # Target SFR


# Polynomial fitting (we use a simple 2nd-degree polynomial for demonstration)
poly = Polynomial.fit(X['ra'], Y, 2)  # Fit a 2nd-degree polynomial


# Get the polynomial coefficients
coeffs = poly.coef


# Find the root(s) of the polynomial (order of zero)
roots = poly.roots()  # This gives the roots, which are the critical points
print("Roots of the fitted polynomial:", roots)
