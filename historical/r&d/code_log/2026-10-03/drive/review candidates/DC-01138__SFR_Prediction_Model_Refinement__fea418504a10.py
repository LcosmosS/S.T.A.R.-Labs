from sklearn.datasets import fetch_california_housing
data = fetch_california_housing(as_frame=True)
X = data.data
y = data.target


                                                                                                                                                                                                                                                                                                                                                                                                                                                   * Use case: Regression (predict housing prices)

                                                                                                                                                                                                                                                                                                                                                                                                                                                   * Pros: Well-structured, clean, no missing values

                                                                                                                                                                                                                                                                                                                                                                                                                                                   * Features: Median income, average rooms, house age, etc.
