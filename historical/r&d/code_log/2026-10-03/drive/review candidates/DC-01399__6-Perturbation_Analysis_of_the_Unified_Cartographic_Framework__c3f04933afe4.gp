phi = (1 + sqrt(5)) / 2;
pi_val = Pi;


\\ List of curves to analyze [a, b] for y^2 = x^3 + ax + b
curves = [[1, 2], [2, 1], [3, 2], [5, 3], [-1706, 6320]];


\\ --- Main Loop ---
for(i = 1, length(curves),
    a = curves[i][1];
    b = curves[i][2];
    print("--------------------------------------------------");
    print("Curve: y^2 = x^3 + ", a, "x + ", b);
    
    \\ Initialize the elliptic curve
    E = ellinit([0, 0, 0, a, b], 1);
    
    \\ Check for singularity
    delta = E.disc;
    print("Discriminant: ", delta);
    if(delta == 0, 
        print("Not an elliptic curve (singular). Skipping."); 
        next
    );
