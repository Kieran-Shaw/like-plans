import os
import re

import numpy as np
import pandas as pd

RAW_PLANS_FILE_PATH = os.path.expanduser("~/like-plans/data/raw/raw_plans.csv")
RAW_PRICINGS_FILE_PATH = os.path.expanduser("~/like-plans/data/raw/raw_pricings.csv")
CLEANED_HMO_EPO_FILE_PATH = os.path.expanduser(
    "~/like-plans/data/processed/hmo_epo_plans.csv"
)
CLEANED_PPO_POS_FILE_PATH = os.path.expanduser(
    "~/like-plans/data/processed/ppo_pos_plans.csv"
)

# list of columns that are included in the model
COLUMNS = [
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

COLUMNS_TO_KEEP = [
    "id",
    "carrier_name",
    "name",
    "hsa_eligible",
    "infertility_treatment_rider",
]

# import the dataframes
plans_df = pd.read_csv(RAW_PLANS_FILE_PATH)
pricings_df = pd.read_csv(RAW_PRICINGS_FILE_PATH)

# set up the dataframe
hmo_df = plans_df[plans_df["plan_type"].isin(["HMO", "EPO"])][COLUMNS].copy()
ppo_df = plans_df[plans_df["plan_type"].isin(["PPO", "POS"])][COLUMNS].copy()


def clean_boolean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.apply(lambda col: col.astype(int) if col.dtype == bool else col)
    return df


def one_hot_encoding():
    return


def clean_hmo_epo_plans(df: pd.DataFrame) -> pd.DataFrame:
    # we clean the HMO and EPO plans differently because they do not have out of network cost sharing, so that would break the similarity model
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
    df["individual_medical_moop_out_of_network"] = (
        df["individual_medical_moop"]
        .apply(lambda x: re.findall(r"Out-of-Network: (\$[\d,]+|Not Covered)", x)[0])
        .replace("Not Covered", np.nan)
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
        .apply(lambda x: re.findall(r"Out-of-Network: (\$[\d,]+|Not Covered)", x)[0])
        .replace("Not Covered", np.nan)
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
            "Not Applicable", None
        )  # what should we do with 'Not Applicable' for coinsurance?
        .replace(
            "$", ""
        )  # I saw that there was a $ sign in one of the coinsurance columns
        .replace("%", "", regex=True)
    )
    return df


def clean_ppo_pos_plans(df: pd.DataFrame) -> pd.DataFrame:
    # we clean the PPO and POS plans differently because, unlike HMO and EPO plans, they have out of network cost sharing
    df["individual_medical_deductible_in_network"] = (
        df["individual_medical_deductible"]
        .apply(lambda x: re.findall(r"In-Network: \$([\d,]+)", x)[0])
        .str.replace(",", "")
        .astype(int)
    )
    df["individual_medical_deductible_out_of_network"] = (
        df["individual_medical_deductible"]
        .apply(lambda x: re.findall(r"Out-of-Network: (\$[\d,]+|Not Covered)", x)[0])
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
        .apply(lambda x: re.findall(r"Out-of-Network: (\$[\d,]+|Not Covered)", x)[0])
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
        .apply(lambda x: re.findall(r"Out-of-Network: (\$[\d,]+|Not Covered)", x)[0])
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
        .apply(lambda x: re.findall(r"Out-of-Network: (\$[\d,]+|Not Covered)", x)[0])
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
        .replace("Not Applicable", None)  # what should we do with 'Not Applicable'?
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
        .replace("Not Applicable", 0)  # what should we do with 'Not Applicable'?
        .replace("$0", 0)
        .replace("%", "", regex=True)
    )

    # drop the columns

    return df


def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_keep = [col for col in COLUMNS if col in COLUMNS_TO_KEEP]
    return_df = df[columns_to_keep].copy()
    return return_df


# apply the methods to the dataframes
hmo_df = clean_ppo_pos_plans(df=hmo_df)
ppo_df = clean_ppo_pos_plans(df=ppo_df)

hmo_df = clean_boolean(df=hmo_df)
ppo_df = clean_boolean(df=ppo_df)

hmo_df = drop_columns(df=hmo_df)
ppo_df = drop_columns(df=ppo_df)

# write the file out
hmo_df.to_csv(CLEANED_HMO_EPO_FILE_PATH, index=False)
ppo_df.to_csv(CLEANED_PPO_POS_FILE_PATH, index=False)
