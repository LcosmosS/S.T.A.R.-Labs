E = ellinit([0, 0, 0, 2, 1], 1); \\ y^2 = x^3 + 2x + 1
gens = ellgenerators(E);
if(length(gens) > 0,
    P = gens[1];
    print("Generator point: ", P);
    height_P = ellheight(E, P);
    print("Height of generator point: ", height_P);
