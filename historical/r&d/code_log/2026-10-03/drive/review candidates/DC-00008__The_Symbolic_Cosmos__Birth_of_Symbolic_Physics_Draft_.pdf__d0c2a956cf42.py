# We will use SageMath to compute the product of Tamagawa numbers.
E = EllipticCurve(QQ, [-1706, 6320])
print(E.tamagawa_numbers())
