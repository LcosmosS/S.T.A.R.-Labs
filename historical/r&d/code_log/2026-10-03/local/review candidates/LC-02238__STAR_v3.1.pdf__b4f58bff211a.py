class StableECCStacker:
    def __init__(self, params):
        from sklearn.linear_model import Lasso, Ridge
        self.base_models = [
            ('xgb', xgb.XGBRegressor(**params)),
            ('lgb', lgb.LGBMRegressor(n_estimators=int(400), verbose=int(-1))),
            ('cat', cb.CatBoostRegressor(iterations=int(400), verbose=int(0)))
