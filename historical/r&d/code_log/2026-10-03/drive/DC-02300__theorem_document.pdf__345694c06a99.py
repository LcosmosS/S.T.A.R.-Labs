from ripser import ripser
from persim import plot_diagrams
def compute_persistence_diagram(positions):
diagrams = ripser(positions)['dgms']
plot_diagrams(diagrams, show=True)
return diagrams
positions = galaxy_data[['x', 'y', 'z']].values
diagrams = compute_persistence_diagram(positions)
