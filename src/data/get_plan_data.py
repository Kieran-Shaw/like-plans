import os

from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

ZIP_CODE = 95030
YEAR = 2023
QUARTER = "Q3"
DESTINATION_PLANS_FILE_PATH = "~/like-plans/data/raw/raw_plans.csv"
DESTINATION_PRICINGS_FILE_PATH = "~/like-plans/data/raw/raw_pricings.csv"
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


# define function to fetch the data from BigQuery
def fetch_bigquery_data(query: str, destination_file_path: str):
    # Create a BigQuery client
    client = bigquery.Client()

    # Run the query and get a pandas DataFrame
    query_job = client.query(query)

    # Get the dataframe as the result
    df = query_job.result().to_dataframe()

    # Save the DataFrame to a file
    df.to_csv(destination_file_path, index=False)
    print(
        f"Saved dataframe from {ZIP_CODE}, {YEAR}, {QUARTER} to {destination_file_path}"
    )
    return


# define the sql query
sql_query_plans = f"""
    WITH SelectedZip AS (
        SELECT * 
        FROM airbyte_ideon.zip_counties
        WHERE zip_code_id = '{ZIP_CODE}'
        AND _ab_source_file_url LIKE '%CA/{YEAR}/{QUARTER}%'
    )
    SELECT
        p.*
    FROM 
        SelectedZip zc
    JOIN 
        airbyte_ideon.plan_counties pc 
        ON zc.county_id = pc.county_id
        AND pc._ab_source_file_url LIKE '%CA/{YEAR}/{QUARTER}%'
    JOIN
        airbyte_ideon.plans p
        ON pc.plan_id = p.id
        AND p._ab_source_file_url LIKE '%CA/{YEAR}/{QUARTER}%';
"""

sql_query_pricings = f"""
    WITH SelectedZip AS (
        SELECT * 
        FROM airbyte_ideon.zip_counties
        WHERE zip_code_id = '{ZIP_CODE}'
        AND _ab_source_file_url LIKE '%CA/{YEAR}/{QUARTER}%'
    )
    SELECT
        pc.plan_id,
        pr.age,
        pr.premium_single
    FROM 
        SelectedZip zc
    JOIN 
        airbyte_ideon.plan_counties pc 
        ON zc.county_id = pc.county_id
        AND pc._ab_source_file_url LIKE '%CA/{YEAR}/{QUARTER}%'
    JOIN
        airbyte_ideon.pricings pr
        ON pc.plan_id = pr.plan_id
        AND zc.rating_area_id = pr.rating_area_id
        AND pr._ab_source_file_url LIKE '%CA/{YEAR}/{QUARTER}%'
"""

# Fetch and save the data
fetch_bigquery_data(
    query=sql_query_plans, destination_file_path=DESTINATION_PLANS_FILE_PATH
)
fetch_bigquery_data(
    query=sql_query_pricings, destination_file_path=DESTINATION_PRICINGS_FILE_PATH
)
