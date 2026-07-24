"""
============================================================
NeuralRetail
Business Recommendation System
============================================================
"""

import os
import joblib
import pandas as pd


class BusinessRecommendation:

    def __init__(self):

        os.makedirs("models", exist_ok=True)
        os.makedirs("images", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)

    # ======================================================
    # PREPARE BUSINESS DATA
    # ======================================================

    def prepare_data(self, df):

        print("\n")
        print("=" * 60)
        print("PREPARING BUSINESS RECOMMENDATION DATA")
        print("=" * 60)

        business = df.groupby(
            ["StockCode", "Description"]
        ).agg({

            "Quantity": "sum",

            "TotalPrice": "sum",

            "CustomerID": "nunique"

        }).reset_index()

        business.columns = [

            "StockCode",

            "Description",

            "QuantitySold",

            "Revenue",

            "UniqueCustomers"

        ]

        print(f"\nTotal Products : {len(business)}")

        return business
        # ======================================================
    # GENERATE BUSINESS RECOMMENDATIONS
    # ======================================================

    def generate_recommendations(self, business):

        print("\nGenerating Business Recommendations...")

        recommendations = []

        for _, row in business.iterrows():

            # Recommendation 1
            if row["QuantitySold"] > 500:

                recommendation = "Increase Inventory"

            # Recommendation 2
            elif row["QuantitySold"] < 100:

                recommendation = "Run Promotional Campaign"

            # Recommendation 3
            elif row["Revenue"] > 5000:

                recommendation = "Increase Product Price"

            # Recommendation 4
            elif row["UniqueCustomers"] > 100:

                recommendation = "Launch Loyalty Program"

            # Default
            else:

                recommendation = "Maintain Current Strategy"

            recommendations.append(recommendation)

        business["Recommendation"] = recommendations

        print("Business Recommendations Generated Successfully")

        return business
        # ======================================================
    # SAVE RECOMMENDATIONS CSV
    # ======================================================

    def save_recommendations(self, business):

        business.to_csv(
            "data/processed/business_recommendations.csv",
            index=False
        )

        print("\nBusiness Recommendations CSV Saved Successfully")
        print("Location : data/processed/business_recommendations.csv")
        # ======================================================
    # SAVE RECOMMENDATION MODEL
    # ======================================================

    def save_model(self, business):

        joblib.dump(
            business,
            "models/recommendation_rules.pkl"
        )

        print("\nRecommendation Model Saved Successfully")
        print("Location : models/recommendation_rules.pkl")

    # ======================================================
    # RECOMMENDATION DISTRIBUTION
    # ======================================================

    def recommendation_distribution(self, business):

        import matplotlib.pyplot as plt

        print("\nGenerating Recommendation Distribution Chart...")

        plt.figure(figsize=(10,6))

        business["Recommendation"].value_counts().plot(
            kind="bar"
        )

        plt.title("Business Recommendation Distribution")

        plt.xlabel("Recommendation")

        plt.ylabel("Number of Products")

        plt.xticks(rotation=20)

        plt.tight_layout()

        plt.savefig(
            "images/recommendation_distribution.png"
        )

        plt.close()

        print("Recommendation Distribution Chart Saved")
        # ======================================================
    # TOP REVENUE PRODUCTS
    # ======================================================

    def top_revenue_products(self, business):

        import matplotlib.pyplot as plt

        print("\nGenerating Top Revenue Products Chart...")

        top = business.nlargest(10, "Revenue")

        plt.figure(figsize=(12,6))

        plt.bar(
            top["Description"],
            top["Revenue"]
        )

        plt.title("Top Revenue Products")

        plt.xlabel("Products")

        plt.ylabel("Revenue")

        plt.xticks(rotation=90)

        plt.tight_layout()

        plt.savefig(
            "images/top_revenue_products.png"
        )

        plt.close()

        print("Top Revenue Products Chart Saved")
        # ======================================================
    # COMPLETE PIPELINE
    # ======================================================

    def run(self, df):

        print("\n")
        print("=" * 60)
        print("BUSINESS RECOMMENDATION SYSTEM")
        print("=" * 60)

        # Step 1 : Prepare Data
        business = self.prepare_data(df)

        # Step 2 : Generate Recommendations
        business = self.generate_recommendations(business)

        # Step 3 : Save CSV
        self.save_recommendations(business)

        # Step 4 : Save Model
        self.save_model(business)

        # Step 5 : Charts
        self.recommendation_distribution(business)

        self.top_revenue_products(business)

        # Summary
        print("\n")
        print("=" * 60)
        print("BUSINESS RECOMMENDATION SYSTEM COMPLETED")
        print("=" * 60)

        print("\nRecommendation Preview\n")

        print(business.head())

        print("\nRecommendation Summary")
        print("-" * 40)

        print(f"Total Products : {len(business)}")

        print("\nRecommendation Counts")

        print(business["Recommendation"].value_counts())

        return business