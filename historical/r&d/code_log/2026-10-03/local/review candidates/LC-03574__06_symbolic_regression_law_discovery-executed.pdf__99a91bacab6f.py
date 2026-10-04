           print("Symbolic regression modules not available; running simple linear␣

        ↪regression fallback.", e)

           from  sklearn.linear_model       import  LinearRegression
           lr  = LinearRegression().fit(X, y)
           preds   = lr.predict(X)
           mse  =  np.mean((preds    -  y)**2)

           pd.DataFrame({'y': y,       'y_pred': preds}).to_csv('results/sr_predictions.

        ↪csv', index=False)
           print("Saved results/sr_predictions.csv (linear fallback). MSE:", mse)

     /__w/S.T.A.R.-Model-for-Mathematical-and-Theoretical-Physics/S.T.A.R.-Model-for-
     Mathematical-and-Theoretical-
