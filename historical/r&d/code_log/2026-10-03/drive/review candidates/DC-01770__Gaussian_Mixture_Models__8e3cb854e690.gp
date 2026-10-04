subpop0 = mass[select(subpopulation==0)];
M0_0 = vecsort(subpop0)[length(subpop0)/2];  // Median
Lk_0 = sum(i=1, length(subpop0), M0_0/subpop0[i]);
