for K in [ZZ, QQ, ComplexField(16), QQ[sqrt(2)], GF(5)]:
    print(K, ":"); print(K['x'](p).factor())