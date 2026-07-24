"""
NeuralRetail
Feature Engineering Module
"""

import pandas as pd
import os


class FeatureEngineering:

    def create_features(self, df):

        print("\n" + "=" * 60)
        print("FEATURE ENGINEERING")
        print("=" * 60)

        # -----------------------------
        # Date Features
        # -----------------------------
        df["Year"] = df["InvoiceDate"].dt.year
        df["Month"] = df["InvoiceDate"].dt.month
        df["MonthName"] = df["InvoiceDate"].dt.month_name()

        df["Quarter"] = df["InvoiceDate"].dt.quarter

        df["Day"] = df["InvoiceDate"].dt.day

        df["DayOfWeek"] = df["InvoiceDate"].dt.dayofweek

        df["DayName"] = df["InvoiceDate"].dt.day_name()

        df["Hour"] = df["InvoiceDate"].dt.hour

        # -----------------------------
        # Weekend Feature
        # -----------------------------
        df["Weekend"] = df["DayOfWeek"].apply(
            lambda x: 1 if x >= 5 else 0
        )

        # -----------------------------
        # Average Order Value
        # -----------------------------
        average_order = (
            df.groupby("CustomerID")["TotalPrice"]
            .transform("mean")
        )

        df["AverageOrderValue"] = average_order

        print("\nNew Features Added Successfully!")

        print("\nCurrent Columns")

        print(df.columns.tolist())

        return df


    def save_dataset(self, df):

        output_path = os.path.join(
            "data",
            "processed",
            "featured_data.csv"
        )

        df.to_csv(output_path, index=False)

        print("\nFeature Engineered Dataset Saved")

        print(output_path)