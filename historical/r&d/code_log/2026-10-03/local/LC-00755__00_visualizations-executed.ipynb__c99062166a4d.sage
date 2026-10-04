try:
    from ripser import ripser
    dgms = ripser(X, maxdim=1)['dgms']
except:
    dgms = None
