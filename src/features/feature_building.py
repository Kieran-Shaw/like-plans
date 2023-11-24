import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class FeatureEngineer:
    def __init__(self, df: pd.DataFrame, exclude_cols=None):
        self.df = df
        self.exclude_cols = exclude_cols if exclude_cols is not None else []
        self.preprocessor = None

    def fit_transform(self):
        # Convert boolean columns to int
        bool_cols = self.df.select_dtypes(include=["bool"]).columns
        self.df[bool_cols] = self.df[bool_cols].astype(int)

        # Exclude certain columns from feature engineering
        df_features = self.df.drop(columns=self.exclude_cols)

        # Determine numerical and categorical columns
        numerical_cols = df_features.select_dtypes(include=["int", "float"]).columns
        categorical_cols = df_features.select_dtypes(include=["object"]).columns

        # Setup transformers
        transformers = [
            ("num", StandardScaler(), numerical_cols),
            ("cat", OneHotEncoder(), categorical_cols),
        ]

        self.preprocessor = ColumnTransformer(transformers)
        return self.preprocessor.fit_transform(df_features)
