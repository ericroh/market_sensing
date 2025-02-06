import pandas as pd

def ensure_datetime(df, column_name='Date'):
    if not pd.api.types.is_datetime64_any_dtype(df[column_name]):
        df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    return df

