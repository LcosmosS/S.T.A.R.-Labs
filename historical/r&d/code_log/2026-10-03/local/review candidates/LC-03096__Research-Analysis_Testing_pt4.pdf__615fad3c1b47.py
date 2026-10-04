            if selmer3_rank is not None and selmer3_rank >= Integer(3):
                if features not in training_data:
                    training_data.append(features)
                    training_labels.append(selmer3_rank)
                    print(f"Found high 3-Selmer rank curve: a={a}, b={b}, 3-Selmer
rank={selmer3_rank}")
    else:
        print("Curve analysis failed, skipping...")

    gc.collect()
    attempt += 1


# Recompute previous curves for plotting
previous_curves = [
    (-1597, 987), (1597, -4181), (2584, 2584), (4181, 6765),
