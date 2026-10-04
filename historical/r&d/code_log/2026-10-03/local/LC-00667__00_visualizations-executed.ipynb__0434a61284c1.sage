fig = px.scatter_3d(
    x=X[:,0], y=X[:,1], z=X[:,2],
    color=entropy,
    color_continuous_scale="Viridis",
    title="Entropy Field (Interactive)"
)
fig.write_html("figures/entropy_interactive.html")
fig.show()
