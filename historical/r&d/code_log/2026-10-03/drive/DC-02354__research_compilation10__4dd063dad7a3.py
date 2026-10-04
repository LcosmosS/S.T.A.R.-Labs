import pandas as pd
   * data = pd.read_csv('your_dataset.csv')
   * Select the relevant columns:
   * python
features = ['log_SFR_Ha', 'log_Mass_gas', 'nsa_mstar', 'log_Mass', 'V-band_SB_at_Re', 
            'vel_sigma_Re', 'OH_Mar13_N2_Re_fit', 'Av_gas_Re']
   * df = data[features]
