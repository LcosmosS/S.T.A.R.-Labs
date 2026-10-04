disc = -16 * (4*a^3 + 27*b^2);
print("Discriminant: ", disc);
conductor = ellglobalred(E)[1];
print("Conductor: ", conductor);
tors = elltors(E);
tors_order = tors[1];
print("Torsion subgroup order: ", tors_order);
