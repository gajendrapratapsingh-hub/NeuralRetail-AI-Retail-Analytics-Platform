"""
===========================================================
NeuralRetail
Price Optimization Module
===========================================================
"""

# =========================================================
# IMPORT LIBRARIES
# =========================================================

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression


# =========================================================
# PRICE OPTIMIZATION CLASS
# =========================================================

class PriceOptimization:

    # -----------------------------------------------------
    # Constructor
    # -----------------------------------------------------

    def __init__(self):

        os.makedirs("models", exist_ok=True)
        os.makedirs("images", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)

    # -----------------------------------------------------
    # Prepare Product Data
    # -----------------------------------------------------

    def prepare_data(self, df):

        print("\n")
        print("=" * 60)
        print("PREPARING PRICE OPTIMIZATION DATA")
        print("=" * 60)

        product_df = (

            df.groupby(["StockCode", "Description"])

            .agg({

                "Quantity": "sum",

                "UnitPrice": "mean",

                "TotalPrice": "sum"

            })

            .reset_index()

        )

        product_df.columns = [

            "StockCode",
            "Description",
            "QuantitySold",
            "CurrentPrice",
            "Revenue"

        ]

        print(f"\nTotal Products : {len(product_df)}")

        print("\nProduct Data Prepared Successfully")

        print("\nPreview:\n")

        print(product_df.head())

        return product_df
        # -----------------------------------------------------
    # Optimize Product Prices
    # -----------------------------------------------------

    def optimize_price(self, product_df):

        print("\nCalculating Price Recommendations...")

        # Features
        X = product_df[["QuantitySold"]]
        y = product_df["CurrentPrice"]

        # Train Simple Linear Regression Model
        model = LinearRegression()
        model.fit(X, y)

        # Predict Recommended Price
        product_df["RecommendedPrice"] = model.predict(X)

        # Prevent Negative Prices
        product_df["RecommendedPrice"] = (
            product_df["RecommendedPrice"]
            .clip(lower=0.10)
            .round(2)
        )

        print("Price Recommendation Completed")

        return product_df, model

    # -----------------------------------------------------
    # Discount Recommendation
    # -----------------------------------------------------

    def recommend_discount(self, product_df):

        print("\nGenerating Discount Recommendations...")

        discounts = []

        for qty in product_df["QuantitySold"]:

            if qty >= 1000:
                discounts.append(0)

            elif qty >= 500:
                discounts.append(5)

            else:
                discounts.append(10)

        product_df["Discount(%)"] = discounts

        print("Discount Recommendation Completed")

        return product_df

    # -----------------------------------------------------
    # Profit Category
    # -----------------------------------------------------

    def profit_category(self, product_df):

        print("\nClassifying Profit Categories...")

        category = []

        for revenue in product_df["Revenue"]:

            if revenue >= 5000:
                category.append("High Profit")

            elif revenue >= 1000:
                category.append("Medium Profit")

            else:
                category.append("Low Profit")

        product_df["ProfitCategory"] = category

        print("Profit Classification Completed")

        return product_df

    # -----------------------------------------------------
    # Save CSV
    # -----------------------------------------------------

    def save_csv(self, product_df):

        output_path = "data/processed/price_optimization.csv"

        product_df.to_csv(
            output_path,
            index=False
        )

        print("\nPrice Optimization CSV Saved Successfully")
        print(f"Location : {output_path}")

    # -----------------------------------------------------
    # Save Model
    # -----------------------------------------------------

    def save_model(self, model):

        model_path = "models/price_optimization_model.pkl"

        joblib.dump(model, model_path)

        print("\nPrice Optimization Model Saved Successfully")
        print(f"Location : {model_path}")

        # -----------------------------------------------------
    # Price Distribution Chart
    # -----------------------------------------------------

    def price_distribution(self, product_df):

        print("\nGenerating Price Distribution Chart...")

        plt.figure(figsize=(10,5))

        plt.hist(
            product_df["CurrentPrice"],
            bins=30,
            edgecolor="black"
        )

        plt.title("Price Distribution")
        plt.xlabel("Price")
        plt.ylabel("Number of Products")

        plt.tight_layout()

        plt.savefig("images/price_distribution.png")

        plt.close()

        print("Price Distribution Chart Saved")

    # -----------------------------------------------------
    # Revenue vs Price
    # -----------------------------------------------------

    def revenue_vs_price(self, product_df):

        print("\nGenerating Revenue vs Price Chart...")

        plt.figure(figsize=(8,6))

        plt.scatter(
            product_df["CurrentPrice"],
            product_df["Revenue"],
            alpha=0.6
        )

        plt.xlabel("Current Price")
        plt.ylabel("Revenue")
        plt.title("Revenue vs Price")

        plt.tight_layout()

        plt.savefig("images/revenue_vs_price.png")

        plt.close()

        print("Revenue vs Price Chart Saved")

    # -----------------------------------------------------
    # Top Profitable Products
    # -----------------------------------------------------

    def top_profitable_products(self, product_df):

        print("\nGenerating Top Profitable Products Chart...")

        top_products = product_df.nlargest(10, "Revenue")

        plt.figure(figsize=(12,6))

        plt.bar(
            top_products["StockCode"].astype(str),
            top_products["Revenue"]
        )

        plt.xticks(rotation=90)

        plt.title("Top 10 Profitable Products")
        plt.xlabel("Stock Code")
        plt.ylabel("Revenue")

        plt.tight_layout()

        plt.savefig("images/top_profitable_products.png")

        plt.close()

        print("Top Profitable Products Chart Saved")

    # -----------------------------------------------------
    # Discount Recommendation Chart
    # -----------------------------------------------------

    def discount_chart(self, product_df):

        print("\nGenerating Discount Recommendation Chart...")

        discount = product_df["Discount(%)"].value_counts().sort_index()

        plt.figure(figsize=(8,5))

        plt.bar(
            discount.index.astype(str),
            discount.values
        )

        plt.xlabel("Discount (%)")
        plt.ylabel("Products")
        plt.title("Discount Recommendation")

        plt.tight_layout()

        plt.savefig("images/discount_recommendation.png")

        plt.close()

        print("Discount Recommendation Chart Saved")

    # -----------------------------------------------------
    # Complete Pipeline
    # -----------------------------------------------------

    def run(self, df):

        print("\n")
        print("=" * 60)
        print("PRICE OPTIMIZATION")
        print("=" * 60)

        product_df = self.prepare_data(df)

        product_df, model = self.optimize_price(product_df)

        product_df = self.recommend_discount(product_df)

        product_df = self.profit_category(product_df)

        self.save_csv(product_df)

        self.save_model(model)

        self.price_distribution(product_df)

        self.revenue_vs_price(product_df)

        self.top_profitable_products(product_df)

        self.discount_chart(product_df)

        print("\n")
        print("=" * 60)
        print("PRICE OPTIMIZATION COMPLETED")
        print("=" * 60)

        print("\nPrice Optimization Preview\n")

        print(product_df.head())

        print("\nPrice Optimization Summary")
        print("-" * 40)

        print(f"Total Products : {len(product_df)}")

        print(
            f"High Profit Products : {(product_df['ProfitCategory']=='High Profit').sum()}"
        )

        print(
            f"Medium Profit Products : {(product_df['ProfitCategory']=='Medium Profit').sum()}"
        )

        print(
            f"Low Profit Products : {(product_df['ProfitCategory']=='Low Profit').sum()}"
        )

        return product_df