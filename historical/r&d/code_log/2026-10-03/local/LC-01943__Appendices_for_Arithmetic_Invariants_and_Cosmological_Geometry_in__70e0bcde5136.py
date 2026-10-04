import  pandas  as  pd  
import  numpy  as  np  
from  pysr  import  PySRRegressor  
from  sklearn.model_selection  import  train_test_split,  cross_val_score  
from  sklearn.metrics  import  r2_score,  mean_absolute_error  
from  sklearn.preprocessing  import  StandardScaler  
from  sklearn.impute  import  SimpleImputer  
from  sklearn.ensemble  import  RandomForestClassifier  
from  xgboost  import  XGBRegressor  
from  imblearn.over_sampling  import  SMOTE  