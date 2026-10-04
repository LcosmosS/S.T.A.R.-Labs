    return study.best_params

# --- 15. Symbolic Regression ---
def run_symbolic_regression(X, y, feature_cols, method='pysr'):
    log_function(f"run_symbolic_regression_{method}")
    if method == 'pysr' and PySRRegressor:
        model = PySRRegressor(
            niterations=40,
            binary_operators=["+", "-", "*", "/"],
            unary_operators=["log", "exp", "sqrt"],
            maxsize=20,
            model_selection="best"
        )
        model.fit(X[feature_cols], y)
        print(f"PySR Equations:\n", model.equations_)
        return model
    elif method == 'gplearn' and SymbolicRegressor:
        model = SymbolicRegressor(
            population_size=1000,
            generations=20,
            function_set=('add', 'sub', 'mul', 'div', 'log', 'sqrt'),
            metric='mse',
            random_state=42
        )
        model.fit(X[feature_cols], y)
        print(f"GPlearn Equation:\n", model._program)
        return model
    else:
        print(f"{method} not installed. Skipping symbolic regression.")
        return None

# --- 16. Interactive Visualization ---
def interactive_visualization(df, feature_cols):
    log_function("interactive_visualization")
    # Altair scatter plot with KDE density
    chart = alt.Chart(df).mark_circle().encode(
        x=alt.X('selmer_rank:Q', title='3-Selmer Rank'),
        y=alt.Y('kde_selmer_rank_var_ap:Q', title='KDE Density (Rank, var_ap)'),
        color='generator_type:N',
        tooltip=['objid', 'logmass', 'petrorad_r', 'selmer_rank', 'selmer_status',
'entropy', 'kde_selmer_rank_var_ap']
    ).interactive().properties(
        width=800, height=400, title='Rank vs. KDE Density by Generator Type'
    )
    chart.save(f'{OUTPUT_PLOT_PREFIX}_interactive_scatter_kde.html')

    # Plotly 3D scatter plot
    fig = px.scatter_3d(
        df, x='logmass', y='entropy', z='kde_selmer_rank_var_ap',
        color='generator_type', size='selmer_rank',
        hover_data=['objid', 'selmer_rank', 'selmer_status', 'entropy',
'kde_selmer_rank_var_ap'],
