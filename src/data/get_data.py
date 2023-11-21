import os
import sys

from dotenv import load_dotenv

from utilities.utils import fetch_bigquery_data, load_sql


class FetchPlansPricings:
    def __init__(self, state, zip_code, year, quarter):
        self.state = state
        self.zip_code = zip_code
        self.year = year
        self.quarter = quarter
        self._setup_environment()
        self._load_sql_queries()

    def _setup_environment(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if self.project_root not in sys.path:
            sys.path.append(self.project_root)
        load_dotenv()
        self.google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    def _load_sql_queries(self):
        self.plans_sql_file_path = os.path.expanduser(
            "~/like-plans/src/utilities/plans.sql"
        )
        self.pricings_sql_file_path = os.path.expanduser(
            "~/like-plans/src/utilities/pricings.sql"
        )
        self.destination_plans_file_path = os.path.expanduser(
            "~/like-plans/data/raw/raw_plans.csv"
        )
        self.destination_pricings_file_path = os.path.expanduser(
            "~/like-plans/data/raw/raw_pricings.csv"
        )

        self.sql_query_plans = load_sql(
            file_path=self.plans_sql_file_path,
            state=self.state,
            zip_code=self.zip_code,
            year=self.year,
            quarter=self.quarter,
        )
        self.sql_query_pricings = load_sql(
            file_path=self.pricings_sql_file_path,
            state=self.state,
            zip_code=self.zip_code,
            year=self.year,
            quarter=self.quarter,
        )

    def fetch_and_save_data(self):
        fetch_bigquery_data(
            query=self.sql_query_plans,
            destination_file_path=self.destination_plans_file_path,
            state=self.state,
            zip_code=self.zip_code,
            year=self.year,
            quarter=self.quarter,
        )
        fetch_bigquery_data(
            query=self.sql_query_pricings,
            destination_file_path=self.destination_pricings_file_path,
            state=self.state,
            zip_code=self.zip_code,
            year=self.year,
            quarter=self.quarter,
        )
