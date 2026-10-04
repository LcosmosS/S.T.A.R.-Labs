    print(f"{regime.capitalize()} Best Equation:", best_eq)



    y_pred = model.predict(X_test_scaled)

    r2 = r2_score(y_test, y_pred)

    mae = mean_absolute_error(y_test, y_pred)

    print(f"{regime.capitalize()} R²: {r2:.4f}, MAE: {mae:.4f}")



    # PNG Scatter (Fixed: Use plt.scatter for mappable)

    fig, ax = plt.subplots(figsize=(10, 6))

    scatter = ax.scatter(X_test['flux_gr'], y_pred, c=X_test['EBV'], cmap='viridis')

    ax.set_title(f'{regime.capitalize()} Projection: g/r Flux vs Predicted z')

    ax.set_xlabel('g/r Flux Ratio')

    ax.set_ylabel('Predicted z')

    plt.colorbar(scatter, label='EBV (Entropy Proxy)')

    plt.savefig(f"visualizations/{regime}_scatter.png")

    plt.close()



    # HTML 3D

    fig = go.Figure(data=go.Scatter3d(

        x=X_test['flux_gr'], y=X_test['flux_rz'], z=y_pred,