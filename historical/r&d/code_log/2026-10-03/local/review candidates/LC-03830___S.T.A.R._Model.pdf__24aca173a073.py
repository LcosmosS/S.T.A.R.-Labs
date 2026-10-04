        else:
            print("No matches found within the specified radius.")

        return df1_matched, df2_matched
    except KeyError as e:
        print(f"KeyError in cross_match: {e}")
        print(f"df1 columns: {df1.columns.tolist()}")
        print(f"df2 columns: {df2.columns.tolist()}")
        raise
    except Exception as e:
        print(f"Error in cross_match: {e}")
        raise

# Store the original DataFrame before cross-matching
df_original = df.copy()

# Cross-match with VizieR catalogues
# SDSS merged dataset (V/147 + V/154, uses RA_ICRS, DE_ICRS)
