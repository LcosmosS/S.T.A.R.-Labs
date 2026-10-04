            if len(chunk_filtered) == 0:
                continue
            # Perform cross-match on the filtered chunk
            _, matched_df2 = cross_match(df1, chunk_filtered, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec)
            if len(matched_df2) > 0:
                matched_df2_list.append(matched_df2[columns_to_keep])
        
        if len(matched_df2_list) == 0:
            print("No matches found in any chunk.")
            return df1, pd.DataFrame()
        
        # Concatenate all matched_df2
        matched_df2 = pd.concat(matched_df2_list, ignore_index=True)
        matched_df1 = df1.copy()
        
        return matched_df1, matched_df2
    except Exception as e:
        print(f"Error in cross_match_in_chunks: {e}")
        raise
