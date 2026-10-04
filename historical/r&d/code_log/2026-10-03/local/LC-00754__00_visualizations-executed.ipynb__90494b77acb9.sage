fig = go.Figure()
fig.add_trace(go.Scatter(x=z, y=H_LCDM, mode='lines', name='ΛCDM'))
fig.add_trace(go.Scatter(x=z, y=H_eff, mode='lines', name='S.T.A.R.'))
fig.update_layout(
    title="Effective Hubble Parameter (Interactive)",
    xaxis_title="z",
    yaxis_title="H(z)"
)
fig.write_html("figures/hubble_interactive.html")
fig.show()
