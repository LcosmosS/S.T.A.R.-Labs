#Define elliptic curve E derived from our cosmological model 
E = EllipticCurve(QQ, [-1706, 6320])


#We will use Sagemath to compute the torsion subgroup 
print(E.torsion_subgroup())
