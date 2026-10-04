# Function to standardize RA/Dec and SpecObj
def standardize_columns(df, cols):
    df = df[cols].copy()
    if 'RA_ICRS' in df.columns and 'DE_ICRS' in df.columns:
        df = df.rename(columns={"RA_ICRS": "objra_y", "DE_ICRS": "objdec"})
    if 'Sp-ID' in df.columns:
        df = df.rename(columns={"Sp-ID": "SpecObj"})
        # Handle plate-MJD-fiber format in Sp-ID
        def convert_plate_mjd_fiber(specid):