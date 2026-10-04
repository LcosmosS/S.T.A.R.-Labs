def define_entropy_strata(x):
   if x < 2.5:
       return 'Low'
   elif 2.5 <= x < 3.0:
       return 'Mid'
   else:
       return 'High'

data['entropy_strata'] = data['L_cosmo(s)'].apply(define_entropy_strata)
