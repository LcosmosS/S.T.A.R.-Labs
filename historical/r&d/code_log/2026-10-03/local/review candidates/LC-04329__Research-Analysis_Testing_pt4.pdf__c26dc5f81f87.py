                reg_diff = abs(filtered_data[i][5] - filtered_data[j][5])

                if reg_diff < 10000:

                    weight = 1 / (1 + reg_diff / 100)

                    ax.plot(

                        [log_deltas[i], log_deltas[j]],

                        [log_conds[i], log_conds[j]],

                        [ranks[i], ranks[j]],

                        'b-',
                        alpha=0.5 * weight,

                        linewidth=0.7 * weight

                    )

            if filtered_data[i][2] >= 2:

                color = 'red' if filtered_data[i][2] == 3 else 'blue'

                ax.text(log_deltas[i], log_conds[i], ranks[i],

                        f'({filtered_data[i][0]},{filtered_data[i][1]}): 54.0 Mly',

                        size=8, color=color)



        ax.set_xlabel('Log(Discriminant)')

        ax.set_ylabel('Log(Conductor)')

        ax.set_zlabel('Rank')

        ax.set_title('Cosmic Interweb: Nodes and Weighted Filaments')

        plt.savefig(f"interweb_plot_attempt_{attempt}.png")

        plt.close()

        print(f"Updated interweb plot saved to interweb_plot_attempt_{attempt}.png")



    attempt += 1



# After collecting data, train a classifier
if len(training_data) >= target_3selmer_curves:

    print(f"\nCollected {len(training_data)} curves with 3-Selmer rank >= 3. Training classifier...")

    # Add some negative examples to balance the dataset

    training_data.extend([
