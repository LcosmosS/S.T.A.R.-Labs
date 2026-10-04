E = ellinit([0, 0, 0, 2, 1]);
gens = ellgenerators(E);
if(length(gens) > 0,
    P = gens[1];
    height_P = ellheight(E, P);
    print("Generator point: ", P);
    print("Height of generator point: ", height_P);
