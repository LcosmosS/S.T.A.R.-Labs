print("Type of M: ", type(M));
* print("Type of Z: ", type(Z));
* They should both be t_VEC (vectors).
* Ensure proper vector creation: If you're creating vectors manually, make sure they are defined correctly. For example:
* pari
* M = vector(N, i, 10^(10.5 + 0.5 * random(1000) / 1000.0));
* This should work, but with real data, you'll replace this with the loaded vector.
