E = EllipticCurve([-1706, 6320])
P = E([2, 54])  # Create the point P = (2, 54) on E
Reg = P.height(prec=100)  # Compute the canonical height with 100 bits of precision
print(Reg)


* E([2, 54]) creates the point P = (2, 54) on the curve ( E ). SageMath will verify that ( (2, 54) ) lies on the curve by checking the equation y^2 = x^3 - 1,706x + 6,320.
* P.height(prec=100) computes the canonical height of ( P ) with 100 bits of precision (approximately 30 decimal places, since \log_{10}(2) \approx 0.301, so 100 bits \approx 100 \times 0.301 \approx 30 decimal places).
