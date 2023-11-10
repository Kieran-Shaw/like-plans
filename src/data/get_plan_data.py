from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()

ZIP_CODE = 95030
YEAR = 2023
QUARTER = 'Q3'
DESTINATION_FILE_PATH = f"~/like-plans/data/raw/raw_plans.csv"
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS

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
    print(f"Saved dataframe of plans from {ZIP_CODE}, {YEAR}, {QUARTER} to {DESTINATION_FILE_PATH}")
    return

# define the sql query
sql_query = f"""
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
        ON p.id = pc.plan_id
        AND p._ab_source_file_url LIKE '%CA/{YEAR}/{QUARTER}%'
"""

# Fetch and save the data
fetch_bigquery_data(query=sql_query, destination_file_path=DESTINATION_FILE_PATH)