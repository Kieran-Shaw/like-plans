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
    ):
        self.feature_clean_plan_df = feature_clean_plan_df
        self.transformed_array = transformed_array
        self.metric = metric
        self.n_neighbors = n_neighbors
        self.model = NearestNeighbors(
            metric=self.metric, n_neighbors=self.n_neighbors + 1
        )
        self.random_plan_df = None
        self.similar_plans_df = None

    def fit(self):
        # Fit the NearestNeighbors model
        self.model.fit(self.transformed_array)

        # Select a random plan
        self.random_plan_df = self.feature_clean_plan_df.sample(n=1)
        random_plan_id = self.random_plan_df["id"].iloc[0]

        # Find the nearest neighbors for the random plan
        random_plan_index = self.random_plan_df.index[0]
        specific_plan_features = self.transformed_array[random_plan_index].reshape(
            1, -1
        )
        distances, indices = self.model.kneighbors(specific_plan_features)

        # Extract indices and distances of similar plans, excluding the first index which is the plan itself
        similar_plans_indices = indices.flatten()[1:]
        similar_plan_distances = distances.flatten()[1:]
        self.similar_plans_df = self.feature_clean_plan_df.iloc[
            similar_plans_indices
        ].copy()

        # Add a column for distances in the similar plans DataFrame
        self.similar_plans_df["similarity_score"] = similar_plan_distances

        # Exclude the random plan using its ID
        self.similar_plans_df = self.similar_plans_df[
            self.similar_plans_df["id"] != random_plan_id
        ]

        # Return the random plan and its similar plans
        return self.random_plan_df, self.similar_plans_df
