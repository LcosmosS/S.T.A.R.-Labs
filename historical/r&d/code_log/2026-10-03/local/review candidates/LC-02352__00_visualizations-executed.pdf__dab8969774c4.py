            from   ripser  import   ripser
            dgms   = ripser(X, maxdim=1)['dgms']
       except:
            dgms   = None

[21]:  if  dgms  is  not  None:
            plt.figure(figsize=(6,5))
            for  d  in  dgms:


                                                        11