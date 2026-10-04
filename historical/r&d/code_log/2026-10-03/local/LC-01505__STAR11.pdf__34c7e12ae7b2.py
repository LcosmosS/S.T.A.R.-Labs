 def  downcast_df(df):      for  col  in  df.select_dtypes(include=['int']).columns:          df[col]  =  pd.to_numeric(df[col],  downcast='integer')      for  col  in  df.select_dtypes(include=['float']).columns:          df[col]  =  pd.to_numeric(df[col],  downcast='float')      return  df  df  =  downcast_df(df)  print(f"Memory  usage  after  downcast:  {df.memory_usage().sum()  /  1024**2:.2f}  MB")   #  Ensure  RA/Dec  are  numeric  and  impute  NaN/infinities  with  medians  
=========================================================================================
===========
