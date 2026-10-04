# Construct symbolic entropy-based projection feature
data['L_cosmo(s)'] = (
   np.log10(data['log_Mass_gas'] + 1e-6) * 
   (1 + data['z'])**0.7 * 
   (data['Smooth'] - data['Featured'])
)
