from sklearn.datasets import fetch_openml
data = fetch_openml(name="house_prices", as_frame=True)
X = data.data.select_dtypes(include=["number"]).dropna(axis=1)
y = data.target


                                                                                                                                                                                                                                                                                                                                                                                                                                                      * Use case: Predict home sale prices

                                                                                                                                                                                                                                                                                                                                                                                                                                                      * Pros: Realistic dataset, many features

                                                                                                                                                                                                                                                                                                                                                                                                                                                      * Note: Needs some preprocessing (especially categorical data)
