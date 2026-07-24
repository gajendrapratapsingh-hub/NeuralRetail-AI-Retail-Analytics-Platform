"""
===========================================================
NeuralRetail
Inventory Optimization Module
===========================================================
"""

import os
import joblib
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


class InventoryOptimization:

    def __init__(self):

        os.makedirs("models", exist_ok=True)
        os.makedirs("images", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)

    # ---------------------------------------------------------
    # Prepare Inventory Data
    # ---------------------------------------------------------
    def prepare_inventory(self, df):

        print("\n" + "=" * 60)
        print("PREPARING INVENTORY DATA")
        print("=" * 60)

        inventory = df.groupby(
            ["StockCode", "Description"]
        ).agg({

            "Quantity": "sum",

            "TotalPrice": "sum"

        }).reset_index()

        inventory.columns = [

            "StockCode",

            "Description",

            "QuantitySold",

            "Revenue"

        ]

        print(f"\nTotal Products : {len(inventory)}")

        return inventory

    # ---------------------------------------------------------
    # Inventory Classification
    # ---------------------------------------------------------
    def classify_inventory(self, inventory):

        print("\nClassifying Products...")

        status = []

        reorder = []

        for qty in inventory["QuantitySold"]:

            if qty >= 1000:

                status.append("Fast Moving")

            elif qty >= 200:

                status.append("Medium Moving")

            else:

                status.append("Slow Moving")

            if qty >= 500:

                reorder.append("YES")

            else:

                reorder.append("NO")

        inventory["InventoryStatus"] = status

        inventory["ReorderAlert"] = reorder

        print("Inventory Classification Completed")

        return inventory
        # ---------------------------------------------------------
    # Save Inventory CSV
    # ---------------------------------------------------------
    def save_inventory(self, inventory):

        output_path = "data/processed/inventory_status.csv"

        inventory.to_csv(output_path, index=False)

        print("\nInventory Status CSV Saved Successfully")
        print(f"Location : {output_path}")

    # ---------------------------------------------------------
    # Top Selling Products
    # ---------------------------------------------------------
    def top_selling_products(self, inventory):

        print("\nGenerating Top Selling Products Chart...")

        top_products = inventory.sort_values(
            by="QuantitySold",
            ascending=False
        ).head(10)

        plt.figure(figsize=(12,6))

        plt.bar(
            top_products["Description"],
            top_products["QuantitySold"]
        )

        plt.title("Top 10 Selling Products")
        plt.xlabel("Products")
        plt.ylabel("Quantity Sold")

        plt.xticks(rotation=90)

        plt.tight_layout()

        plt.savefig("images/top_selling_products.png")

        plt.close()

        print("Top Selling Products Chart Saved")

    # ---------------------------------------------------------
    # Inventory Status Pie Chart
    # ---------------------------------------------------------
    def inventory_status_chart(self, inventory):

        print("\nGenerating Inventory Status Chart...")

        status = inventory["InventoryStatus"].value_counts()

        plt.figure(figsize=(7,7))

        plt.pie(
            status.values,
            labels=status.index,
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Inventory Status Distribution")

        plt.tight_layout()

        plt.savefig("images/inventory_status.png")

        plt.close()

        print("Inventory Status Chart Saved")

    # ---------------------------------------------------------
    # Low Stock Products
    # ---------------------------------------------------------
    def low_stock_products(self, inventory):

        print("\nGenerating Low Stock Products Chart...")

        low_stock = inventory[
            inventory["InventoryStatus"] == "Slow Moving"
        ].head(10)

        plt.figure(figsize=(12,6))

        plt.bar(
            low_stock["Description"],
            low_stock["QuantitySold"]
        )

        plt.title("Top Low Selling Products")
        plt.xlabel("Products")
        plt.ylabel("Quantity Sold")

        plt.xticks(rotation=90)

        plt.tight_layout()

        plt.savefig("images/low_stock_products.png")

        plt.close()

        print("Low Stock Products Chart Saved")
    # ---------------------------------------------------------
    # Save Model (Project Consistency)
    # ---------------------------------------------------------
    def save_model(self, inventory):

        model_path = "models/inventory_model.pkl"

        joblib.dump(inventory, model_path)

        print("\nInventory Model Saved Successfully")
        print(f"Location : {model_path}")

    # ---------------------------------------------------------
    # Complete Pipeline
    # ---------------------------------------------------------
    def run(self, df):

        print("\n")
        print("=" * 60)
        print("INVENTORY OPTIMIZATION")
        print("=" * 60)

        # Step 1 : Prepare Inventory Data
        inventory = self.prepare_inventory(df)

        # Step 2 : Inventory Classification
        inventory = self.classify_inventory(inventory)

        # Step 3 : Save CSV
        self.save_inventory(inventory)

        # Step 4 : Save Model
        self.save_model(inventory)

        # Step 5 : Charts
        self.top_selling_products(inventory)

        self.inventory_status_chart(inventory)

        self.low_stock_products(inventory)

        print("\n")
        print("=" * 60)
        print("INVENTORY OPTIMIZATION COMPLETED")
        print("=" * 60)

        print("\nInventory Preview\n")
        print(inventory.head())

        print("\nInventory Summary")
        print("-" * 40)

        print(f"Total Products : {len(inventory)}")

        print(f"Fast Moving Products : {(inventory['InventoryStatus']=='Fast Moving').sum()}")

        print(f"Medium Moving Products : {(inventory['InventoryStatus']=='Medium Moving').sum()}")

        print(f"Slow Moving Products : {(inventory['InventoryStatus']=='Slow Moving').sum()}")

        print(f"Reorder Alerts : {(inventory['ReorderAlert']=='YES').sum()}")

        return inventory