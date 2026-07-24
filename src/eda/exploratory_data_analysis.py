"""
NeuralRetail
Exploratory Data Analysis
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns


class ExploratoryDataAnalysis:

    def __init__(self):
        os.makedirs("images", exist_ok=True)

    # -------------------------------------
    # Monthly Sales
    # -------------------------------------
    def monthly_sales(self, df):

        monthly = df.groupby("Month")["TotalPrice"].sum()

        plt.figure(figsize=(10,5))
        plt.plot(monthly.index, monthly.values, marker="o")
        plt.title("Monthly Sales")
        plt.xlabel("Month")
        plt.ylabel("Revenue")
        plt.grid(True)

        plt.savefig("images/monthly_sales.png")
        plt.close()

        print("✅ Monthly Sales Chart Saved")

    # -------------------------------------
    # Top 10 Products
    # -------------------------------------
    def top_products(self, df):

        products = (
            df.groupby("Description")["Quantity"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        plt.figure(figsize=(12,6))
        products.plot(kind="bar")

        plt.title("Top 10 Products")
        plt.ylabel("Quantity Sold")

        plt.tight_layout()

        plt.savefig("images/top_products.png")
        plt.close()

        print("✅ Top Products Chart Saved")

    # -------------------------------------
    # Top 10 Customers
    # -------------------------------------
    def top_customers(self, df):

        customers = (
            df.groupby("CustomerID")["TotalPrice"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        plt.figure(figsize=(10,5))
        customers.plot(kind="bar")

        plt.title("Top Customers")
        plt.ylabel("Revenue")

        plt.tight_layout()

        plt.savefig("images/top_customers.png")
        plt.close()

        print("✅ Top Customers Chart Saved")

    # -------------------------------------
    # Sales by Country
    # -------------------------------------
    def country_sales(self, df):

        country = (
            df.groupby("Country")["TotalPrice"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        plt.figure(figsize=(12,6))
        country.plot(kind="bar")

        plt.title("Top 10 Countries")

        plt.ylabel("Revenue")

        plt.tight_layout()

        plt.savefig("images/country_sales.png")

        plt.close()

        print("✅ Country Sales Chart Saved")

    # -------------------------------------
    # Correlation Heatmap
    # -------------------------------------
    def correlation_heatmap(self, df):

        numeric = df.select_dtypes(include="number")

        plt.figure(figsize=(10,8))

        sns.heatmap(
            numeric.corr(),
            annot=True,
            cmap="coolwarm"
        )

        plt.title("Correlation Heatmap")

        plt.tight_layout()

        plt.savefig("images/correlation_heatmap.png")

        plt.close()

        print("✅ Correlation Heatmap Saved")