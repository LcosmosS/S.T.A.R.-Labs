from sklearn.preprocessing import PolynomialFeatures


features = ['log_Mass_gas', 'nsa_mstar', 'OH_Mar13_N2_Re_fit', 'Av_gas_Re']
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(df[features])
poly_feature_names = poly.get_feature_names_out(features)
df_poly = pd.DataFrame(X_poly, columns=poly_feature_names)
