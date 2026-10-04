E = ellinit([-1706, 6320]);  \\ Define the curve
elltors(E)  \\ Torsion subgroup
gr = ellglobalred(E);  \\ Global reduction data
tamagawa = [[gr[4][i,1], gr[5][i][4]] | i<-[1..#gr[4][,1]]];  \\ Tamagawa numbers
prod([t[2] | t <- tamagawa])  \\ Product of Tamagawa numbers
