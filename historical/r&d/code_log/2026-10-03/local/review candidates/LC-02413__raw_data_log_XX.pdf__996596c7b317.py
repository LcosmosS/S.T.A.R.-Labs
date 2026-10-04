from sage.all import * pari.allocatemem(3000000000) from sage.parallel.decorate import parallel
E_coma = EllipticCurve(QQ, [-10141, 9980]) # Predicted curve for Coma rank_coma =
E_coma.rank() # Algebraic rank via 2-descent print(f"Predicted Rank: {rank_coma}") if
