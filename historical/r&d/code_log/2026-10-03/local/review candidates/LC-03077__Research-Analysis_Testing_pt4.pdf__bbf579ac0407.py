            if selmer3_rank is not None and selmer3_rank >= Integer(3):
                if features not in training_data:
                    training_data.append(features)
                    training_labels.append(selmer3_rank)
                    print(f"Found high 3-Selmer rank curve: a={a}, b={b}, 3-Selmer rank={selmer3_rank}")
    else:
        print("Curve analysis failed, skipping...")

    # Memory позволя management
    gc.collect()
    attempt += 1

# Recompute previous curves for plotting (Attempts 71–86, simplified)
previous_curves = [
