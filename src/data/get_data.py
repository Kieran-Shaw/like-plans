import os
import sys

from dotenv import load_dotenv

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from utilities.utils import fetch_bigquery_data, load_sql

load_dotenv()

STATE = "CA"
ZIP_CODE = 95030
YEAR = 2023
QUARTER = "Q1"
PLANS_SQL_FILE_PATH = os.path.expanduser("~/like-plans/src/utilities/plans.sql")
PRICINGS_SQL_FILE_PATH = os.path.expanduser("~/like-plans/src/utilities/pricings.sql")
DESTINATION_PLANS_FILE_PATH = os.path.expanduser("~/like-plans/data/raw/raw_plans.csv")
DESTINATION_PRICINGS_FILE_PATH = os.path.expanduser(
    "~/like-plans/data/raw/raw_pricings.csv"
)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# load the sql scripts
sql_query_plans = load_sql(
    file_path=PLANS_SQL_FILE_PATH,
    state=STATE,
    zip_code=ZIP_CODE,
    year=YEAR,
    quarter=QUARTER,
)
sql_query_pricings = load_sql(
    file_path=PRICINGS_SQL_FILE_PATH,
    state=STATE,
    zip_code=ZIP_CODE,
    year=YEAR,
    quarter=QUARTER,
)

# Fetch and save the raw data
fetch_bigquery_data(
    query=sql_query_plans,
    destination_file_path=DESTINATION_PLANS_FILE_PATH,
    state=STATE,
    zip_code=ZIP_CODE,
    year=YEAR,
    quarter=QUARTER,
)
fetch_bigquery_data(
    query=sql_query_pricings,
    destination_file_path=DESTINATION_PRICINGS_FILE_PATH,
    state=STATE,
    zip_code=ZIP_CODE,
    year=YEAR,
    quarter=QUARTER,
)
