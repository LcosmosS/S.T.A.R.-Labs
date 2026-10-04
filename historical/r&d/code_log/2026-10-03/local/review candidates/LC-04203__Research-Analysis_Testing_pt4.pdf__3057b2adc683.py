            for feat in rank3_features:
                synth_feat = [f + random.gauss(0, 0.4) for f in feat]
                X_data.append(synth_feat)
                y_data.append(1)
        classifier.fit(np.array(X_data), np.array(y_data))
        print(f"Classifier trained. Coefficients: {classifier.coef_}")
