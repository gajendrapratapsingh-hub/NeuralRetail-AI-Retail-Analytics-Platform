"""
NeuralRetail
Data Cleaning Module
"""

import pandas as pd
import os


class DataCleaning:

    def clean_dataset(self, df):

        print("\n" + "=" * 60)
        print("STARTING DATA CLEANING")
        print("=" * 60)

        print(f"\nOriginal Shape : {df.shape}")

        # -----------------------------
        # Remove Duplicate Rows
        # -----------------------------
        duplicate_rows = df.duplicated().sum()

        print(f"\nDuplicate Rows Found : {duplicate_rows}")

        df = df.drop_duplicates()

        # -----------------------------
        # Remove Missing Description
        # -----------------------------
        missing_description = df["Description"].isnull().sum()

        print(f"Missing Description : {missing_description}")

        df = df.dropna(subset=["Description"])

        # -----------------------------
        # Remove Missing CustomerID
        # -----------------------------
        missing_customer = df["CustomerID"].isnull().sum()

        print(f"Missing CustomerID : {missing_customer}")

        df = df.dropna(subset=["CustomerID"])

        # -----------------------------
        # Remove Cancelled Orders
        # -----------------------------
        cancelled_orders = df["InvoiceNo"].astype(str).str.startswith("C").sum()

        print(f"Cancelled Orders : {cancelled_orders}")

        df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

        # -----------------------------
        # Remove Invalid Quantity
        # -----------------------------
        invalid_quantity = (df["Quantity"] <= 0).sum()

        print(f"Invalid Quantity : {invalid_quantity}")

        df = df[df["Quantity"] > 0]

        # -----------------------------
        # Remove Invalid UnitPrice
        # -----------------------------
        invalid_price = (df["UnitPrice"] <= 0).sum()

        print(f"Invalid Unit Price : {invalid_price}")

        df = df[df["UnitPrice"] > 0]

        # -----------------------------
        # Convert InvoiceDate
        # -----------------------------
        df["InvoiceDate"] = pd.to_datetime(
            df["InvoiceDate"],
            dayfirst=True
        )

        # -----------------------------
        # Create TotalPrice
        # -----------------------------
        df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

        print(f"\nFinal Shape : {df.shape}")

        print("\nData Cleaning Completed Successfully")

        return df

    def save_dataset(self, df):

        output_path = os.path.join(
            "data",
            "processed",
            "clean_data.csv"
        )

        df.to_csv(output_path, index=False)

        print(f"\nClean Dataset Saved Successfully")

        print(f"Location : {output_path}")