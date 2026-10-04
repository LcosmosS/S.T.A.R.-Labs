import plotly.express as px
fig = px.scatter_3d(df, x='log_SFR_Ha', y='log_Mass', z='nsa_mstar')
fig.show()
