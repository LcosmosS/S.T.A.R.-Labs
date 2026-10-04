    y_data.append(success)


    if success and rank is not None:


        interweb_data.append((-1706, 6320, rank, features[2], features[3]))





# Save interweb data


with open("interweb_nodes.txt", "w") as f:


    f.write("a,b,rank,log_delta,log_cond\n")


    for a, b, rank, log_delta, log_cond in interweb_data:


        f.write(f"{a},{b},{rank},{log_delta},{log_cond}\n")





print(f"\nCompleted: {successful_curves} successful curves analyzed out of {attempts} attempts")


if X_data:


    print("\nFinal classifier data summary:")


    print(f"Total curves analyzed: {len(X_data)}")


    print(f"Success rate: {sum(y_data) / len(y_data):.2%}")


if interweb_data:


    print("\nInterweb nodes saved to interweb_nodes.txt")

    print("Sample nodes:", interweb_data[:2])
