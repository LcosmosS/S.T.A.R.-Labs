E = ellinit([0, 0, 0, 1, 2]); \\ y^2 = x^3 + x + 2
gens = ellgenerators(E);
if(length(gens) > 0, 
    P = gens[1];
    height_P = ellheight(E, P);
    print("Height of generator point: ", height_P);
