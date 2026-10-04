E = ellinit([-1706, 6320]);
elltors(E);
gr = ellglobalred(E);
tamagawa = [[gr[4][i,1], gr[5][i][4]] | i<-[1..#gr[4][,1]]];
prod([t[2] | t <- tamagawa]);
