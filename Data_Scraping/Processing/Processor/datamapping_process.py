import pandas as pd

def filter_and_map_data(raw_df, ref_df, lookup_col="lookup_key", output_file="mapped_output.csv"):
    if raw_df is None or ref_df is None:
        print("[DataMapping Process] Input dataframes are empty.")
        return False

    try:
        # Ensure uniqueness in raw data
        unique_keys = raw_df[lookup_col].drop_duplicates()

        # Filter reference data based on those keys
        mapped_df = ref_df[ref_df[lookup_col].isin(unique_keys)]

        if mapped_df.empty:
            print("[DataMapping Process] No matches found.")
            return False

        mapped_df.to_csv(output_file, index=False)
        print(f"[DataMapping Process] Mapped data saved to {output_file} with {len(mapped_df)} rows.")
        return True
    except Exception as e:
        print(f"[DataMapping Process] Error during processing: {e}")
        return False
