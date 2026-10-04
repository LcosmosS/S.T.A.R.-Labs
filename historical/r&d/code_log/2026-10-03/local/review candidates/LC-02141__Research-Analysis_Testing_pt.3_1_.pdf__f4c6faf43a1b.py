with open("interweb_nodes.txt", "w") as f:


    f.write("a,b,rank,normalized_leading_coeff,omega,regulator,tamagawa,log_delta,log_cond\n")


    for a, b, rank, lc, omega, reg, tamagawa, ld, lcnd in interweb_data:


        f.write(f"{a},{b},{rank},{lc},{omega},{reg},{tamagawa},{ld},{lcnd}\n")





print(f"\nCompleted: {successful_curves} successful curves analyzed out of {attempts} attempts")