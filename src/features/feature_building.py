import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class FeatureEngineer:
    def __init__(self, exclude_cols: list = None):
        self.exclude_cols = exclude_cols if exclude_cols is not None else []
        self.preprocessor = None

    def fit_transform(self, df: pd.DataFrame):
        # Convert boolean columns to int
        bool_cols = df.select_dtypes(include=["bool"]).columns
        df[bool_cols] = df[bool_cols].astype(int)

        # Exclude certain columns from feature engineering
        df_features = df.drop(columns=self.exclude_cols)

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

    def calculate_primary_care_physician(
        self,
        dollar_values,
        percentages,
        initial_visits,
        assumed_pcp_service_charge: float = 171.0,
        assumed_pcp_yearly_visits: int = 3,
    ):
        # Ensure dollar_values and percentages are all floats
        dollar_values = [
            float(val)
            for val in dollar_values
            if isinstance(val, (int, float, str)) and val not in [None, ""]
        ]
        percentages = [
            float(val)
            for val in percentages
            if isinstance(val, (int, float, str)) and val not in [None, ""]
        ]
        # Calculate average dollar value
        dollar_avg = 0.0
        if initial_visits > 0 and len(dollar_values) > 1:
            remaining_visits = max(assumed_pcp_yearly_visits - initial_visits, 0)
            dollar_avg = (
                (initial_visits * dollar_values[0])
                + (remaining_visits * dollar_values[1])
            ) / assumed_pcp_yearly_visits
        elif dollar_values:
            dollar_avg = sum(dollar_values) / len(dollar_values)

        # Calculate average percentage value
        percent_avg = 0.0
        if percentages:
            percent_avg = (
                (sum(percentages) / len(percentages)) * assumed_pcp_service_charge / 100
            )

        # Combine the calculated values
        if len(dollar_values) > 1 and percent_avg > 0:
            value = (dollar_avg + percent_avg) / 2
        elif dollar_avg > 0:
            value = dollar_avg
        else:
            value = percent_avg

        return value

    def drop_hmo_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        columns_to_drop = [
            "individual_medical_deductible",
            "family_medical_deductible",
            "individual_medical_moop",
            "family_medical_moop",
            "plan_coinsurance",
            "individual_drug_deductible",
            "family_drug_deductible",
            "primary_care_physician",
            "primary_care_physician_in_network_cleaned",
            "pcp_cleaned_dollar_values_in_network",
            "pcp_cleaned_percentages_in_network",
            "pcp_initial_visits_in_network",
        ]
        return df.drop(columns=columns_to_drop)
    
    def drop_ppo_columns(self, df:pd.DataFrame) -> pd.DataFrame:
        columns_to_drop = [
            "individual_medical_deductible",
            "family_medical_deductible",
            "individual_medical_moop",
            "family_medical_moop",
            "plan_coinsurance",
            "individual_drug_deductible",
            "family_drug_deductible",
            "primary_care_physician",
            "primary_care_physician_in_network_cleaned",
            "pcp_cleaned_dollar_values_in_network",
            "pcp_cleaned_percentages_in_network",
            "pcp_initial_visits_in_network",
            "primary_care_physician_out_of_network_cleaned",
            "pcp_cleaned_dollar_values_out_of_network",
            "pcp_cleaned_percentages_out_of_network",
            "pcp_initial_visits_out_of_network",
        ]
        return df.drop(columns=columns_to_drop)
