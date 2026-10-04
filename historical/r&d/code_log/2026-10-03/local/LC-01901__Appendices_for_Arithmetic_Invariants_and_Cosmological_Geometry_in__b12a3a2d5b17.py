df_clust  =  df[df['z']  >=  0.1]  
if  len(df_clust)  <  len(df_gal)  /  10:   #  Balance  if  too  small  
    df_clust  =  pd.concat([df_clust]  *  2)   #  Oversample  
 
#  PySR  function  
def  run_pysr(X,  y,  regime):  
    model  =  PySRRegressor(  
        niterations=200,  
        binary_operators=["+",  "-",  "*",  "/",  "pow"],  
        unary_operators=["log",  "exp",  "sqrt"],  
        extra_sympy_mappings={'inv':  lambda  x:  1/x},  
        elementwise_loss="loss(prediction,  target)  =  (prediction  -  target)^2",  
        model_selection="best",  
        complexity_of_operators={"pow":  3,  "exp":  2,  "log":  2},  
        maxsize=25,  
        maxdepth=5,  
        parsimony=0.01,  
        random_state=42,  
        deterministic=True,  
        parallelism='serial',  