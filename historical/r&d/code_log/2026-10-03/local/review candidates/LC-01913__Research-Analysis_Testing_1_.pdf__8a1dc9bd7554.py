Tamagawa = prod(E.tamagawa_numbers())
P = E.point([2, 54])
Reg = P.height()
Sha_estimate = 5.71614727018219 / (Omega * Reg * Tamagawa)
print(Omega, Reg, Tamagawa, Sha_estimate)


        Without these values, we can’t compute |\text{Sha}(E)|, but the cosmological
