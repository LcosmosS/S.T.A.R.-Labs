            if selmer3_rank >= Integer(3):
                training_data.append(features)
                training_labels.append(selmer3_rank)
                print(f"Added twisted curve to training data: {features}, label: {selmer3_rank}")
except Exception as e:
    print(f"Failed to compute rank of twisted curve: {e}")

# Improved cosmic interweb plot without adjust_text
print("\nGenerating improved cosmic interweb plot...")
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    interweb_data = [(a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
math.log(abs(E.discriminant())), math.log(E.conductor()),
                      (omega * reg * (VIRGO_DISTANCE / (omega * SQRT_KAPPA))**3) / (1e12 if rank == 3
else 5e13 if rank == 2 else 1e15 if rank == 1 else 1e13))
