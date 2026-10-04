def bsd_predicted_sfr(logmass, z):
    a, b, c = 0.5, -0.1, 0.0  # Example coefficients; replace with actual values
*     return a * logmass + b * z + c
* Next Steps: Rerun the script with the updated formula. Check the new MSE in the console and the observed_vs_predicted_sfr.png plot:
   * If MSE Drops: A significant reduction in MSE (e.g., from 0.5 to 0.1) indicates the BSD model aligns better with observations, suggesting it’s on the right track.
   * If MSE Remains High: The formula may need additional terms (e.g., mass-dependent or redshift-dependent factors) to improve fit.
