           from  ripser   import   ripser
           from  persim   import   plot_diagrams
           D  = np.linalg.norm(points[:,None,:]         -  points[None,:,:], axis=2)
           diagrams   =  ripser(D, distance_matrix=True, maxdim=1)['dgms']
           plot_diagrams(diagrams, show=True)
           print("Computed persistence diagrams (ripser).")
      except   Exception   as  e:
           print("ripser/persim not available or failed:", e)










                                                        5
