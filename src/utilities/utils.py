from google.cloud import bigquery


def fetch_bigquery_data(
    query: str,
    destination_file_path: str,
    state: str,
    zip_code: int,
    year: int,
    quarter: str,
) -> None:
    # Create a BigQuery client
    client = bigquery.Client()

    # Run the query and get a pandas DataFrame
    query_job = client.query(query)

    # Get the dataframe as the result
    df = query_job.result().to_dataframe()

    # Save the DataFrame to a file
    df.to_csv(destination_file_path, index=False)

    # print the results
    print(
        f"Saved dataframe from {state}, {zip_code}, {year}, {quarter} to {destination_file_path}"
    )
    return


def load_sql(file_path, **kwargs):
    with open(file_path, "r") as file:
        query = file.read()
        return query.format(**kwargs)
