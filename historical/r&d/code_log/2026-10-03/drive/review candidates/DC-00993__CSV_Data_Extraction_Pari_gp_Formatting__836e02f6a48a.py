import pandas as pd
                                                * df['group'] = pd.cut(df['logmass'], bins=4, labels=['Low', 'Mid-Low', 'Mid-High', 'High'])
