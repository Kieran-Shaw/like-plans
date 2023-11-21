import pandas as pd


def clean_boolean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.apply(lambda col: col.astype(int) if col.dtype == bool else col)
    return df


def one_hot_encoding(df: pd.DataFrame) -> pd.DataFrame:
    # one hot encoding
    # I don't need to worry about n-1 dummy variables because cosine similarity measures the orientation of similarity, not the magnitude. When measuring the magnitude, multicollinearity is important.
    # All n categories are important here, so we can measure the similarity across all categories.

    one_hot_encoding_columns = ["level", "plan_type"]

    # thinking that I should dynamically find the one hot encoding columns
    df_encoded = pd.get_dummies(
        df,
        columns=one_hot_encoding_columns,
    )

    return df_encoded
