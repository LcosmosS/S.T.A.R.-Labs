#  PySR  and  Boosting  per  regime  
def  run_models(X,  y,  regime):  
    X  =  imputer.fit_transform(X)  
    X_train,  X_test,  y_train,  y_test  =  train_test_split(X,  y,  test_size=0.2,  random_state=42)  
    scaler  =  StandardScaler()  
    X_train_scaled  =  scaler.fit_transform(X_train)  
    X_test_scaled  =  scaler.transform(X_test)  
     
    #  PySR  
    pysr_model  =  PySRRegressor(  
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