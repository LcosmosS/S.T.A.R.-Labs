a = -1; b = 1;
E = ellinit([0, a, 0, b, 0]);
periods = ellperiods(E, 1);
omega = periods[1];
print("Omega: ", omega);
