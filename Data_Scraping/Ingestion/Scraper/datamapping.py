import pandas as pd

def read_raw_and_reference(raw_file='raw_data.csv', reference_file='reference_data.xlsx'):
    try:
        raw_df = pd.read_csv(raw_file)
        ref_df = pd.read_excel(reference_file, engine="openpyxl")
        return raw_df, ref_df
    except Exception as e:
        print(f"[DataMapping] Error reading files: {e}")
        return None, None
