import pandas as pd


# Remove duplicate rows
def remove_duplicates(df):
    return df.drop_duplicates()


# Remove rows with missing values
def remove_missing(df):
    return df.dropna()


# Rename columns (remove spaces, convert to lowercase)
def rename_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


# Convert date columns automatically
def convert_dates(df):

    for col in df.columns:

        try:
            df[col] = pd.to_datetime(df[col], errors="ignore")
        except:
            pass

    return df


# Encode categorical columns
def encode_categorical(df):

    categorical = df.select_dtypes(include="object").columns

    for col in categorical:
        df[col] = df[col].astype("category").cat.codes

    return df