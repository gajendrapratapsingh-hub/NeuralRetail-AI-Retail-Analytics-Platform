"""
============================================================
NeuralRetail
Model Evaluation
============================================================
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


class ModelEvaluation:

    def __init__(self):

        os.makedirs("data/processed", exist_ok=True)
        os.makedirs("images", exist_ok=True)

    # ======================================================
    # CUSTOMER SEGMENTATION EVALUATION
    # ======================================================

    def evaluate_segmentation(self):

        print("\nEvaluating Customer Segmentation...")

        try:

            segments = pd.read_csv(
                "data/processed/customer_segments.csv"
            )

            if "Cluster" in segments.columns:

                total_clusters = segments["Cluster"].nunique()

            else:

                total_clusters = 0

            print(f"Total Clusters : {total_clusters}")

            return {
                "Module": "Customer Segmentation",
                "Metric": "Total Clusters",
                "Value": total_clusters
            }

        except Exception as e:

            print("Segmentation Evaluation Failed")

            return {
                "Module": "Customer Segmentation",
                "Metric": "Total Clusters",
                "Value": "N/A"
            }
    # ======================================================
    # SALES FORECAST EVALUATION
    # ======================================================

    def evaluate_forecasting(self):

        print("\nEvaluating Sales Forecasting...")

        try:

            forecast = pd.read_csv(
                "data/processed/forecasted_sales.csv"
            )

            total_predictions = len(forecast)

            print(f"Forecast Records : {total_predictions}")

            return {
                "Module": "Sales Forecasting",
                "Metric": "Forecast Records",
                "Value": total_predictions
            }

        except Exception:

            print("Forecast Evaluation Failed")

            return {
                "Module": "Sales Forecasting",
                "Metric": "Forecast Records",
                "Value": "N/A"
            }
    # ======================================================
    # CUSTOMER CHURN EVALUATION
    # ======================================================

    def evaluate_churn(self):

        print("\nEvaluating Customer Churn...")

        try:

            churn = pd.read_csv(
                "data/processed/churn_prediction.csv"
            )

            total_customers = len(churn)

            print(f"Customers Evaluated : {total_customers}")

            return {
                "Module": "Customer Churn",
                "Metric": "Customers Evaluated",
                "Value": total_customers
            }

        except Exception:

            print("Churn Evaluation Failed")

            return {
                "Module": "Customer Churn",
                "Metric": "Customers Evaluated",
                "Value": "N/A"
            }
    # ======================================================
    # INVENTORY EVALUATION
    # ======================================================

    def evaluate_inventory(self):

        print("\nEvaluating Inventory...")

        try:

            inventory = pd.read_csv(
                "data/processed/inventory_status.csv"
            )

            total_products = len(inventory)

            print(f"Products Evaluated : {total_products}")

            return {
                "Module": "Inventory",
                "Metric": "Products Evaluated",
                "Value": total_products
            }

        except Exception:

            print("Inventory Evaluation Failed")

            return {
                "Module": "Inventory",
                "Metric": "Products Evaluated",
                "Value": "N/A"
            }
    # ======================================================
    # PRICE OPTIMIZATION EVALUATION
    # ======================================================

    def evaluate_price(self):

        print("\nEvaluating Price Optimization...")

        try:

            pricing = pd.read_csv(
                "data/processed/price_optimization.csv"
            )

            total_products = len(pricing)

            print(f"Products Evaluated : {total_products}")

            return {
                "Module": "Price Optimization",
                "Metric": "Products Evaluated",
                "Value": total_products
            }

        except Exception:

            print("Price Evaluation Failed")

            return {
                "Module": "Price Optimization",
                "Metric": "Products Evaluated",
                "Value": "N/A"
            }
    # ======================================================
    # COLLECT ALL EVALUATION RESULTS
    # ======================================================

    def collect_results(self):

        print("\nCollecting Evaluation Results...")

        results = []

        results.append(self.evaluate_segmentation())

        results.append(self.evaluate_forecasting())

        results.append(self.evaluate_churn())

        results.append(self.evaluate_inventory())

        results.append(self.evaluate_price())

        evaluation_df = pd.DataFrame(results)

        print("Evaluation Results Collected Successfully")

        return evaluation_df
    # ======================================================
    # SAVE EVALUATION REPORT
    # ======================================================

    def save_report(self, evaluation_df):

        evaluation_df.to_csv(

            "data/processed/model_evaluation.csv",

            index=False

        )

        print("\nModel Evaluation Report Saved Successfully")

        print("Location : data/processed/model_evaluation.csv")
 
    # ======================================================
    # COMPLETE PIPELINE
    # ======================================================

    def run(self):

        print("\n")
        print("=" * 60)
        print("MODEL EVALUATION")
        print("=" * 60)

        # Step 1 : Collect Results
        evaluation_df = self.collect_results()

        # Step 2 : Save Report
        self.save_report(evaluation_df)

        # Step 3 : Generate Charts
        self.module_comparison_chart(evaluation_df)

        self.model_scores_chart(evaluation_df)

        # Final Summary
        print("\n")
        print("=" * 60)
        print("MODEL EVALUATION COMPLETED")
        print("=" * 60)

        print("\nEvaluation Report\n")

        print(evaluation_df)

        return evaluation_df