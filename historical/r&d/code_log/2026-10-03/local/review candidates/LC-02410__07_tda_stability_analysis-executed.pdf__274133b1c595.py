           L  = np.load('results/tda_landscape.npy')

           plt.figure(figsize=(6,4))
           if  L.ndim   == 2:
                for  i  in range(min(3, L.shape[0])):
                     plt.plot(L[i], label=f'layer_{i}')
           else:
                plt.plot(L)

           plt.title('Persistence Landscape (sample)')
           plt.savefig('results/persistence_landscape.png', dpi=200)
           plt.show()

           print("Saved results/persistence_landscape.png")

      except   Exception   as  e:
           print("No landscape to plot:", e)
















                                                        3