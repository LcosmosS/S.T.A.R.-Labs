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
import  plotly.graph_objects  as  go  
import  matplotlib.pyplot  as  plt  
import  seaborn  as  sns  
import  os  
from  matplotlib  import  cm  
from  sklearn.linear_model  import  LinearRegression   #  Optional  fallback  
 
pd.set_option('mode.chained_assignment',  None)  