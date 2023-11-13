import re

import numpy as np
import pandas as pd

RAW_PLANS_FILE_PATH = "~/like-plans/data/raw/raw_plans.csv"
RAW_PRICINGS_FILE_PATH = "~/like-plans/data/raw/raw_pricings.csv"
CLEANED_FILE_PATH = "~/like-plans/data/processed/plans.csv"

# just storing this list of columns to keep for reference
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
    "preventative_care",
]

# import the dataframes
plans_df = pd.read_csv(RAW_PLANS_FILE_PATH)
pricings_df = pd.read_csv(RAW_PRICINGS_FILE_PATH)

# set up the dataframe
df = plans_df[COLUMNS].copy()

# clean the medical deductible
df["individual_medical_deductible_in_network"] = (
    df["individual_medical_deductible"]
    .apply(lambda x: re.findall(r"In-Network: \$([\d,]+)", x)[0])
    .str.replace(",", "")
    .astype(int)
)
df["individual_medical_deductible_out_of_network"] = (
    df["individual_medical_deductible"]
    .apply(lambda x: re.findall(r"Out-of-Network: (\$[\d,]+|Not Covered)", x)[0])
    .replace("Not Covered", np.nan)
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
    .replace("Not Covered", np.nan)
    .str.replace("$", "")
    .str.replace(",", "")
)

# clean the max out of pocket
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

# clean the coinsurance columns
df["coinsurance_in_network"] = (
    df["plan_coinsurance"]
    .apply(
        lambda x: re.findall(r"In-Network: (\d+%|\$0|Not Applicable)", x)[0]
        if re.findall(r"In-Network: (\d+%|\$0|Not Applicable)", x)
        else None
    )
    .replace("Not Applicable", None)
    .replace("$0", 0)
    .replace("%", "", regex=True)
)
df["coinsurance_out_of_network"] = (
    df["plan_coinsurance"]
    .apply(
        lambda x: re.findall(r"Out-of-Network: (\d+%|\$0|Not Applicable)", x)[0]
        if re.findall(r"Out-of-Network: (\d+%|\$0|Not Applicable)", x)
        else None
    )
    .replace("Not Applicable", None)
    .replace("$0", 0)
    .replace("%", "", regex=True)
)

# preventative care
df["preventative_care_in_network"] = (
    df["preventative_care"]
    .apply(lambda x: re.findall(r"In-Network: \$([\d,]+)", x)[0])
    .astype(int)
)
# need to add preventative care out of network (I can create some encodings or I could impute the value??)

# drop the columns not needed
df.drop(
    columns=[
        "individual_medical_deductible",
        "family_medical_deductible",
        "individual_medical_moop",
        "family_medical_moop",
        "plan_coinsurance",
    ],
    inplace=True,
)


# write the file out
df.to_csv(CLEANED_FILE_PATH, index=False)
