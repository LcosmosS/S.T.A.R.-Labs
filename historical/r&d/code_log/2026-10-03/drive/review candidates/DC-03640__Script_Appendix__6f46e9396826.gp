E = ellinit([-1706, 6320]);  \\ Define the curve
elltors(E)  \\ Torsion subgroup
gr = ellglobalred(E);  \\ Global reduction data
tamagawa = [[gr[i,1], gr[i]] | i<-[1..#gr[,1]]];  \\ Tamagawa numbers
prod([t | t <- tamagawa])  \\ Product of Tamagawa numbers
