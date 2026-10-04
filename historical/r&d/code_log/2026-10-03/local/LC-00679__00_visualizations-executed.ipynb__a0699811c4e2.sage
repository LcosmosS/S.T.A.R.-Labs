if dgms is not None:
    plt.figure(figsize=(6,5))
    for d in dgms:
        plt.scatter(d[:,0], d[:,1], s=10)
    plt.title("Persistence Diagram")
    plt.savefig('figures/persistence_diagram.png', dpi=200)
    plt.show()
