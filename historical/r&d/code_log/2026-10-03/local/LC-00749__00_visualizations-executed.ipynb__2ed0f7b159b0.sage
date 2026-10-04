fig = go.Figure()
for g in geos:
    fig.add_trace(go.Scatter3d(
        x=g[:,0], y=g[:,1], z=g[:,2],
        mode='lines',
        line=dict(width=4)
    ))
fig.update_layout(title="Symbolic Geodesics (Interactive)")
fig.write_html("figures/geodesics_interactive.html")
fig.show()
