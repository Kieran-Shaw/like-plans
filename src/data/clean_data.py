import os
import re

import numpy as np
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
            "individual_drug_deductible",
            "family_drug_deductible",
            "primary_care_physician",
            "network_size",
        ]

    def read_data(self) -> pd.DataFrame:
        return pd.read_csv(self.raw_file_path)

    def save_data(self, df: pd.DataFrame) -> None:
        df.to_csv(self.cleaned_file_path, index=False)
        return


class HMOEPOCleaner(PlanCleaner):
    HMO_EPO_CLEANED_FILE_PATH = os.path.expanduser(
        "~/like-plans/data/processed/hmo_epo_plans_cleaned.csv"
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
        ).astype(int)
        df["individual_drug_deductible_in_network"] = df[
            "individual_drug_deductible"
        ].apply(
            lambda x: 0
            if "included in medical" in x.lower()
            else int(re.findall(r"In-Network: \$([\d,]+)", x)[0].replace(",", ""))
            if re.findall(r"In-Network: \$([\d,]+)", x)
            else None
        )  # 'included in medical' should be a $0 deductible
        df["family_drug_deductible_in_network"] = df["family_drug_deductible"].apply(
            lambda x: 0
            if "included in medical" in x.lower()
            else int(re.findall(r"In-Network: \$([\d,]+)", x)[0].replace(",", ""))
            if re.findall(r"In-Network: \$([\d,]+)", x)
            else None
        )  # 'included in medical' should be a $0 deductible
        df["primary_care_physician_in_network_cleaned"] = df[
            "primary_care_physician"
        ].apply(
            lambda x: re.search(r"In-Network: (.+?) /", x).group(1)
            if re.search(r"In-Network: (.+?) /", x)
            else None
        )

        # apply the primary care physician cleaning
        (
            df["pcp_cleaned_dollar_values_in_network"],
            df["pcp_cleaned_percentages_in_network"],
            df["pcp_initial_visits_in_network"],
            df["pcp_after_deductible_in_network"],
        ) = zip(
            *df["primary_care_physician_in_network_cleaned"].apply(
                self.clean_primary_care_physician
            )
        )
        return df

    def clean_primary_care_physician(self, value: str):
        # Extract dollar amounts
        dollar_values = [
            float(val) for val in re.findall(r"(?<=\$)(\d+)(?:\.\d+)?", value)
        ]

        # Extract percentages
        percentages = [
            float(val) for val in re.findall(r"(\d+)(?:\.\d+)?(?=\%)", value)
        ]

        # Extract the number of initial visits
        initial_visits = re.search(r"first (\d+) visit", value)
        initial_visits = int(initial_visits.group(1)) if initial_visits else 0

        # Find after deductible
        after_deductible = "after deductible" in value.lower()

        return dollar_values, percentages, initial_visits, after_deductible


class PPOPOSCleaner(PlanCleaner):
    PPO_POS_CLEANED_FILE_PATH = os.path.expanduser(
        "~/like-plans/data/processed/ppo_pos_plans_cleaned.csv"
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
        ).astype(int)
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
        ).astype(int)
        # included in medical is a $0 drug deductible
        df["individual_drug_deductible_in_network"] = df[
            "individual_drug_deductible"
        ].apply(
            lambda x: 0
            if "included in medical" in x.lower()
            else int(re.findall(r"In-Network: \$([\d,]+)", x)[0].replace(",", ""))
            if re.findall(r"In-Network: \$([\d,]+)", x)
            else None
        )
        df["family_drug_deductible_in_network"] = df["family_drug_deductible"].apply(
            lambda x: 0
            if "included in medical" in x.lower()
            else int(re.findall(r"In-Network: \$([\d,]+)", x)[0].replace(",", ""))
            if re.findall(r"In-Network: \$([\d,]+)", x)
            else None
        )
        df["primary_care_physician_in_network_cleaned"] = df[
            "primary_care_physician"
        ].apply(
            lambda x: re.search(r"In-Network: (.+?) /", x).group(1)
            if re.search(r"In-Network: (.+?) /", x)
            else None
        )
        df["primary_care_physician_out_of_network_cleaned"] = df[
            "primary_care_physician"
        ].apply(
            lambda x: re.search(r"Out-of-Network: (.+)$", x).group(1)
            if re.search(r"Out-of-Network: (.+)$", x)
            else None
        )

        # apply the primary care physician cleaning
        (
            df["pcp_cleaned_dollar_values_in_network"],
            df["pcp_cleaned_percentages_in_network"],
            df["pcp_initial_visits_in_network"],
            df["pcp_after_deductible_in_network"],
        ) = zip(
            *df["primary_care_physician_in_network_cleaned"].apply(
                self.clean_primary_care_physician
            )
        )
        (
            df["pcp_cleaned_dollar_values_out_of_network"],
            df["pcp_cleaned_percentages_out_of_network"],
            df["pcp_initial_visits_out_of_network"],
            df["pcp_after_deductible_out_of_network"],
        ) = zip(
            *df["primary_care_physician_out_of_network_cleaned"].apply(
                self.clean_primary_care_physician
            )
        )

        return df

    def clean_primary_care_physician(self, value: str):
        # Extract dollar amounts
        dollar_values = [
            float(val) for val in re.findall(r"(?<=\$)(\d+)(?:\.\d+)?", value)
        ]

        # Extract percentages
        percentages = [
            float(val) for val in re.findall(r"(\d+)(?:\.\d+)?(?=\%)", value)
        ]

        # Extract the number of initial visits
        initial_visits = re.search(r"first (\d+) visit", value)
        initial_visits = int(initial_visits.group(1)) if initial_visits else 0

        # Find after deductible
        after_deductible = "after deductible" in value.lower()

        return dollar_values, percentages, initial_visits, after_deductible
