import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


class MedicalPlanSimilarityModel:
    def __init__(
        self,
        feature_clean_plan_df: pd.DataFrame,
        transformed_array: np.ndarray,
        metric: str,
        n_neighbors: int,
        plan_id: str = None,  # Optional plan_id parameter
        carrier_name: str = None,  # Optional carrier_id parameter
    ):
        self.feature_clean_plan_df = feature_clean_plan_df
        self.transformed_array = transformed_array
        self.metric = metric
        self.n_neighbors = n_neighbors
        self.model = NearestNeighbors(
            metric=self.metric, n_neighbors=self.n_neighbors + 1
        )
        self.plan_id = plan_id
        self.carrier_name = carrier_name  # Store the provided carrier_id
        self.similar_plans_df = None

    def fit(self):
        # Fit the NearestNeighbors model
        self.model.fit(self.transformed_array)

        if self.plan_id is None:
            # Select a random plan if no plan_id is provided
            selected_plan_df = self.feature_clean_plan_df.sample(n=1)
        else:
            # Select the specific plan if plan_id is provided
            selected_plan_df = self.feature_clean_plan_df[
                self.feature_clean_plan_df["id"] == self.plan_id
            ]
            if selected_plan_df.empty:
                raise ValueError(f"No plan found with ID: {self.plan_id}")

        selected_plan_id = selected_plan_df["id"].iloc[0]

        # Find the nearest neighbors for the selected plan
        selected_plan_index = selected_plan_df.index[0]
        specific_plan_features = self.transformed_array[selected_plan_index].reshape(
            1, -1
        )
        distances, indices = self.model.kneighbors(specific_plan_features)

        # Extract indices and distances of similar plans
        similar_plans_indices = indices.flatten()[1:]
        similar_plan_distances = distances.flatten()[1:]
        self.similar_plans_df = self.feature_clean_plan_df.iloc[
            similar_plans_indices
        ].copy()

        # Add a column for distances in the similar plans DataFrame
        self.similar_plans_df["similarity_score"] = similar_plan_distances

        # Filter the similar plans based on the carrier_id if provided
        if self.carrier_name:
            self.similar_plans_df = self.similar_plans_df[
                self.similar_plans_df["carrier_name"] == self.carrier_name
            ]

        # Exclude the selected plan using its ID
        self.similar_plans_df = self.similar_plans_df[
            self.similar_plans_df["id"] != selected_plan_id
        ]

        # Return the selected plan and its similar plans
        return selected_plan_df, self.similar_plans_df
