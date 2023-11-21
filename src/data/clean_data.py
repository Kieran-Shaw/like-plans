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


def one_hot_encoding(df: pd.DataFrame) -> pd.DataFrame:
    # one hot encoding
    # I don't need to worry about n-1 dummy variables because cosine similarity measures the orientation of similarity, not the magnitude. When measuring the magnitude, multicollinearity is important.
    # All n categories are important here, so we can measure the similarity across all categories.

    one_hot_encoding_columns = ["level", "plan_type"]
    df_encoded = pd.get_dummies(
        df,
        columns=one_hot_encoding_columns,
    )

    return df_encoded


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

    # drop the columns
    columns_to_drop = [
        "individual_medical_deductible",
        "family_medical_deductible",
        "individual_medical_moop",
        "family_medical_moop",
        "plan_coinsurance",
    ]
    df.drop(columns=columns_to_drop, inplace=True)
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
    columns_to_drop = [
        "individual_medical_deductible",
        "family_medical_deductible",
        "individual_medical_moop",
        "family_medical_moop",
        "plan_coinsurance",
    ]
    df.drop(columns=columns_to_drop, inplace=True)

    return df


# apply the methods to the dataframes
hmo_df = clean_hmo_epo_plans(df=hmo_df)
ppo_df = clean_ppo_pos_plans(df=ppo_df)

hmo_df = one_hot_encoding(df=hmo_df)
ppo_df = one_hot_encoding(df=ppo_df)

hmo_df = clean_boolean(df=hmo_df)
ppo_df = clean_boolean(df=ppo_df)

# hmo_df = drop_columns(df=hmo_df)
# ppo_df = drop_columns(df=ppo_df)

# write the file out
hmo_df.to_csv(CLEANED_HMO_EPO_FILE_PATH, index=False)
ppo_df.to_csv(CLEANED_PPO_POS_FILE_PATH, index=False)
