cv_scores_gen  =  cross_val_score(gen_clf,  X_clf,  y_gen,  cv=5)  
print("Generator  Classifier  CV  Mean  Accuracy:",  cv_scores_gen.mean())  
gen_clf.fit(X_clf,  y_gen)  
df['predicted_type']  =  gen_clf.predict(X_clf)  
 
#  Balance  
smote  =  SMOTE(random_state=42)  
X_res,  y_res  =  smote.fit_resample(X_clf,  y_clf)  
 
#  Regime  split  
df_gal  =  df[df['predicted_regime']  ==  0]  
df_clust  =  df[df['predicted_regime']  ==  1]  
 
#  Models  function  
def  run_models(X,  y,  regime):  
    X  =  imputer.fit_transform(X)  
    X_train,  X_test,  y_train,  y_test  =  train_test_split(X,  y,  test_size=0.2,  random_state=42)  
    scaler  =  StandardScaler()  
    X_train_scaled  =  scaler.fit_transform(X_train)  
    X_test_scaled  =  scaler.transform(X_test)  