            # Derive curve
            a = -round(31.59259 * r)
            E = EllipticCurve(QQ, [a, b])
            E.two_descent(second_limit=20, verbose=False)
            rank = E.rank(only_use_mwrank=False)
            gens = E.gens()
            P = gens[0] if rank > 0 else None

            # Dichotomy
            gen_type = classify_generator_type(P)
            if gen_type is None: continue

            # Extract numerators/denominators
            if P:
                x, y, z = P
                x, y = x/z, y/z
                num_x, den_x = x.numerator(), x.denominator()
                num_y, den_y = y.numerator(), y.denominator()
            else:
                num_x = num_y = den_x = den_y = np.nan

            data.append({
                "name": name,
                "r": r, "rho": rho, "rho_star": rho_star,
                "a": a, "b": b, "rank": rank,
                "gen_type": gen_type,
                "num_x": float(num_x), "num_y": float(num_y),
                "den_x": float(den_x), "den_y": float(den_y)
            })
        except:
            continue
    return pd.DataFrame(data)

# ————————————————————————
# 4. ML PIPELINE
# ————————————————————————
def run_ml_pipeline(df):
    # Features
    X = df[["r", "rho_star", "rank"]].values
    y_type = df["gen_type"].map({"Simple": 0, "Recursive": 1}).values

    # Split
    X_train, X_test, y_train_type, y_test_type = train_test_split(
        X, y_type, test_size=0.3, random_state=42, stratify=y_type
    )

    # ——— CLASSIFIER: Predict Dichotomy ———
    clf = XGBRegressor(n_estimators=100, random_state=42)