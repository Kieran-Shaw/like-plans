import re

import pandas as pd

RAW_PLANS_FILE_PATH = "~/like-plans/data/processed/raw_plans.csv"
RAW_PRICINGS_FILE_PATH = "~/like-plans/data/processed/raw_pricings.csv"

# just storing this list of columns to keep for reference
COLUMNS = [
    "id",
    "carrier_name",
    "name",
    "level",
    "plan_type",
    "individual_medical_deductible",
    "family_medical_deductible",
]

# import the dataframes
plans_df = pd.read_csv(RAW_PLANS_FILE_PATH)
pricings_df = pd.read_csv(RAW_PRICINGS_FILE_PATH)

# set up the dataframe
df = plans_df[COLUMNS]
# cleaning script
df = plans_df[COLUMNS]

# clean the medical deductible
df["individual_medical_deductible_in_network"] = (
    df["individual_medical_deductible"]
    .apply(lambda x: re.findall(r"In-Network: \$([\d,]+)", x)[0])
    .str.replace(",", "")
    .astype(int)
)

df["individual_medical_deductible_out_of_network"] = (
    df["individual_medical_deductible"]
    .apply(lambda x: re.findall(r"Out-of-Network: \$([\d,]+)", x)[0])
    .str.replace(",", "")
    .astype(int)
)

# ah wait, sometimes out of network services aren't covered / don't have any dollar amount associated... how should I handle?
df["family_medical_deductible_in_network"] = (
    df["family_medical_deductible"]
    .apply(lambda x: re.findall(r"In-Network: \$([\d,]+)", x)[0])
    .str.replace(",", "")
    .astype(int)
)

df["family_medical_deductible_out_of_network"] = (
    df["family_medical_deductible"]
    .apply(lambda x: re.findall(r"Out-of-Network: \$([\d,]+)", x)[0])
    .str.replace(",", "")
    .astype(int)
)

# drop the columns we don't need
df.drop(columns=["individual_medical_deductible", "family_medical_deductible"])
