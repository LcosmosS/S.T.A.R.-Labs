if (abs(left_side - right_side) < tolerance * right_side,
    print("Cosmological BSD analogue holds within 10%"),
    print("Cosmological BSD analogue fails: Left side != Right side")
)
