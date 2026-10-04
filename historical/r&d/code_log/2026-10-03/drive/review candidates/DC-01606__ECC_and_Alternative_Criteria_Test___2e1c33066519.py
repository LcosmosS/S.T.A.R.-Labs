    print("cypari2 not installed. Run: mamba install cypari2 -c conda-forge") 
    exit(1) 
try: 
    from gudhi.weighted_rips_complex import WeightedRipsComplex 
    from gudhi import plot_persistence_diagram 
    import gudhi 
