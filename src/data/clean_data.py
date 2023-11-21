import os
import re

import pandas as pd


class PlanCleaner:
    # This base class can be extended by HMOEPOCleaner and PPOPOSCleaner
    def __init__(self) -> None:
        self.raw_file_path = os.path.expanduser("~/like-plans/data/raw/raw_plans.csv")
        self.columns = [
            "id",
            "carrier_name",
            "name",
            "level",
            "plan_type",
            "individual_medical_deductible",
            "family_medical_deductible",
            "individual_medical_moop",
            "family_medical_moop",
            "plan_coinsurance",
            "hsa_eligible",
            "infertility_treatment_rider",
        ]

    def read_data(self) -> pd.DataFrame:
        return pd.read_csv(self.raw_file_path)

    def save_data(self, df: pd.DataFrame) -> None:
        df.to_csv(self.cleaned_file_path, index=False)
        return

    def drop_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        columns_to_drop = [
            "individual_medical_deductible",
            "family_medical_deductible",
            "individual_medical_moop",
            "family_medical_moop",
            "plan_coinsurance",
        ]
        return df.drop(columns=columns_to_drop)


class HMOEPOCleaner(PlanCleaner):
    HMO_EPO_CLEANED_FILE_PATH = os.path.expanduser(
        "~/like-plans/data/processed/hmo_epo_plans.csv"
    )

    def __init__(self):
        super().__init__()
        self.cleaned_file_path = self.HMO_EPO_CLEANED_FILE_PATH

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[df["plan_type"].isin(["HMO", "EPO"])][self.columns].copy()

        df["individual_medical_deductible_in_network"] = (
            df["individual_medical_deductible"]
            .apply(lambda x: re.findall(r"In-Network: \$([\d,]+)", x)[0])
            .str.replace(",", "")
            .astype(int)
        )
        df["family_medical_deductible_in_network"] = (
            df["family_medical_deductible"]
            .apply(lambda x: re.findall(r"In-Network: \$([\d,]+)", x)[0])
            .str.replace(",", "")
            .astype(int)
        )
        df["individual_medical_moop_in_network"] = (
            df["individual_medical_moop"]
            .apply(lambda x: re.findall(r"In-Network: \$([\d,]+)", x)[0])
            .str.replace(",", "")
            .astype(int)
        )
        df["family_medical_moop_in_network"] = (
            df["family_medical_moop"]
            .apply(lambda x: re.findall(r"In-Network: \$([\d,]+)", x)[0])
            .str.replace(",", "")
            .astype(int)
        )
        df["coinsurance_in_network"] = (
            df["plan_coinsurance"]
            .apply(
                lambda x: re.findall(r"In-Network: (\d+%|\$0|Not Applicable)", x)[0]
                if re.findall(r"In-Network: (\d+%|\$0|Not Applicable)", x)
                else None
            )
            .replace("Not Applicable", 0)  # if not applicable, normalize to 0
            .replace(
                "$", ""
            )  # I saw that there was a $ sign in one of the coinsurance columns
            .replace("%", "", regex=True)
        )

        # drop columns
        df = self.drop_columns(df=df)
        return df


class PPOPOSCleaner(PlanCleaner):
    PPO_POS_CLEANED_FILE_PATH = os.path.expanduser(
        "~/like-plans/data/processed/ppo_pos_plans.csv"
    )

    def __init__(self):
        super().__init__()
        self.cleaned_file_path = self.PPO_POS_CLEANED_FILE_PATH

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[df["plan_type"].isin(["PPO", "POS"])][self.columns].copy()

        df["individual_medical_deductible_in_network"] = (
            df["individual_medical_deductible"]
            .apply(lambda x: re.findall(r"In-Network: \$([\d,]+)", x)[0])
            .str.replace(",", "")
            .astype(int)
        )
        df["individual_medical_deductible_out_of_network"] = (
            df["individual_medical_deductible"]
            .apply(
                lambda x: re.findall(r"Out-of-Network: (\$[\d,]+|Not Covered)", x)[0]
            )
            .str.replace("$", "")
            .str.replace(",", "")
        )
        df["family_medical_deductible_in_network"] = (
            df["family_medical_deductible"]
            .apply(lambda x: re.findall(r"In-Network: \$([\d,]+)", x)[0])
            .str.replace(",", "")
            .astype(int)
        )
        df["family_medical_deductible_out_of_network"] = (
            df["family_medical_deductible"]
            .apply(
                lambda x: re.findall(r"Out-of-Network: (\$[\d,]+|Not Covered)", x)[0]
            )
            .str.replace("$", "")
            .str.replace(",", "")
        )
        df["individual_medical_moop_in_network"] = (
            df["individual_medical_moop"]
            .apply(lambda x: re.findall(r"In-Network: \$([\d,]+)", x)[0])
            .str.replace(",", "")
            .astype(int)
        )
        df["individual_medical_moop_out_of_network"] = (
            df["individual_medical_moop"]
            .apply(
                lambda x: re.findall(r"Out-of-Network: (\$[\d,]+|Not Covered)", x)[0]
            )
            .str.replace("$", "")
            .str.replace(",", "")
        )
        df["family_medical_moop_in_network"] = (
            df["family_medical_moop"]
            .apply(lambda x: re.findall(r"In-Network: \$([\d,]+)", x)[0])
            .str.replace(",", "")
            .astype(int)
        )
        df["family_medical_moop_out_of_network"] = (
            df["family_medical_moop"]
            .apply(
                lambda x: re.findall(r"Out-of-Network: (\$[\d,]+|Not Covered)", x)[0]
            )
            .str.replace("$", "")
            .str.replace(",", "")
        )
        df["coinsurance_in_network"] = (
            df["plan_coinsurance"]
            .apply(
                lambda x: re.findall(r"In-Network: (\d+%|\$0|Not Applicable)", x)[0]
                if re.findall(r"In-Network: (\d+%|\$0|Not Applicable)", x)
                else None
            )
            .replace(
                "Not Applicable", 0
            )  # if coinsurance is not applicable, lets normalize to 0 for the time being
            .replace("\$", "", regex=True)
            .replace("%", "", regex=True)
        )
        df["coinsurance_out_of_network"] = (
            df["plan_coinsurance"]
            .apply(
                lambda x: re.findall(r"Out-of-Network: (\d+%|\$0|Not Applicable)", x)[0]
                if re.findall(r"Out-of-Network: (\d+%|\$0|Not Applicable)", x)
                else None
            )
            .replace(
                "Not Applicable", 0
            )  # if not applicable for OON for ppo_pos plans, lets normalize to 0
            .replace("$0", 0)
            .replace("%", "", regex=True)
        )

        # drop the columns
        df = self.drop_columns(df=df)
        return df
