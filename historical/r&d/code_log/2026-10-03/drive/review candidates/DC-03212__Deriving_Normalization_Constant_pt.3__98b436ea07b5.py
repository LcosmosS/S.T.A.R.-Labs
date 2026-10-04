if (abs(left_side - right_side) < tolerance * right_side,
    print("Cosmological BSD analogue holds within 10%"),
    print("Cosmological BSD analogue fails: Left side != Right side")
)
The error messages indicate that PARI/GP expects )->, ,, or ) at certain points, and the lack of a semicolon causes an "unexpected end of file" error. This suggests that PARI/GP is confused about where the statement ends without the semicolon.
