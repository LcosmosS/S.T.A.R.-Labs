    print("The pipeline cannot proceed to the validation stage.")
    exit()

if df.empty or len(df) < 2:
    print(f"\n\033[91mCRITICAL PIPELINE ERROR:\033[0m")
