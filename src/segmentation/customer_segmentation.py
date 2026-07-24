"""
===========================================================
NeuralRetail
Customer Segmentation using RFM + KMeans
===========================================================
"""

import os
import joblib
import pandas as pd
import matplotlib

# Prevent matplotlib from opening GUI windows
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


class CustomerSegmentation:

    def __init__(self):

        os.makedirs("models", exist_ok=True)
        os.makedirs("images", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)
        os.makedirs("reports", exist_ok=True)

    # ---------------------------------------------------------
    # Create RFM Features
    # ---------------------------------------------------------
    def create_rfm(self, df):

        print("\n" + "=" * 60)
        print("CREATING RFM FEATURES")
        print("=" * 60)

        latest_date = df["InvoiceDate"].max()

        rfm = df.groupby("CustomerID").agg({
            "InvoiceDate": lambda x: (latest_date - x.max()).days,
            "InvoiceNo": "nunique",
            "TotalPrice": "sum"
        })

        rfm.columns = ["Recency", "Frequency", "Monetary"]

        print("\nRFM Features Created Successfully")
        print(rfm.head())

        return rfm

    # ---------------------------------------------------------
    # Elbow Method
    # ---------------------------------------------------------
    def elbow_method(self, scaled_data):

        print("\nFinding Optimal Number of Clusters...")

        inertia = []

        for k in range(1, 11):

            model = KMeans(
                n_clusters=k,
                random_state=42,
                n_init=10
            )

            model.fit(scaled_data)

            inertia.append(model.inertia_)

        plt.figure(figsize=(8, 5))

        plt.plot(range(1, 11), inertia, marker="o")

        plt.title("Elbow Method")
        plt.xlabel("Number of Clusters")
        plt.ylabel("WCSS")
        plt.grid(True)

        plt.tight_layout()

        plt.savefig("images/elbow_method.png")

        plt.close()

        print("Elbow Method Graph Saved")

    # ---------------------------------------------------------
    # Train KMeans Model
    # ---------------------------------------------------------
    def train_model(self, rfm):

        print("\n" + "=" * 60)
        print("TRAINING KMEANS MODEL")
        print("=" * 60)

        scaler = StandardScaler()

        scaled = scaler.fit_transform(rfm)

        # Generate Elbow Graph
        self.elbow_method(scaled)

        # Train Model
        kmeans = KMeans(
            n_clusters=4,
            random_state=42,
            n_init=10
        )

        clusters = kmeans.fit_predict(scaled)

        rfm["Cluster"] = clusters

        # -------------------------------
        # Silhouette Score
        # -------------------------------
        score = silhouette_score(scaled, clusters)

        print("\n" + "=" * 60)
        print(f"Silhouette Score : {score:.4f}")
        print("=" * 60)

        with open("reports/silhouette_score.txt", "w") as file:
            file.write(f"Silhouette Score : {score:.4f}")

        print("Silhouette Score Saved")

        # Save Model
        joblib.dump(kmeans, "models/kmeans_model.pkl")

        print("KMeans Model Saved Successfully")

        return rfm
        # ---------------------------------------------------------
    # Save Customer Segments
    # ---------------------------------------------------------
    def save_segments(self, rfm):

        output_path = "data/processed/customer_segments.csv"

        rfm.to_csv(output_path)

        print("\nCustomer Segments Saved Successfully")
        print(f"Location : {output_path}")

    # ---------------------------------------------------------
    # Cluster Distribution Chart
    # ---------------------------------------------------------
    def cluster_distribution(self, rfm):

        plt.figure(figsize=(8, 5))

        rfm["Cluster"].value_counts().sort_index().plot(
            kind="bar"
        )

        plt.title("Cluster Distribution")
        plt.xlabel("Cluster")
        plt.ylabel("Number of Customers")

        plt.tight_layout()

        plt.savefig("images/cluster_distribution.png")

        plt.close()

        print("Cluster Distribution Graph Saved")

    # ---------------------------------------------------------
    # Customer Segments Scatter Plot
    # ---------------------------------------------------------
    def customer_segments(self, rfm):

        plt.figure(figsize=(8, 6))

        scatter = plt.scatter(
            rfm["Recency"],
            rfm["Monetary"],
            c=rfm["Cluster"],
            cmap="viridis"
        )

        plt.xlabel("Recency")
        plt.ylabel("Monetary")
        plt.title("Customer Segments")

        plt.colorbar(scatter)

        plt.tight_layout()

        plt.savefig("images/customer_segments.png")

        plt.close()

        print("Customer Segments Plot Saved")

    # ---------------------------------------------------------
    # Complete Pipeline
    # ---------------------------------------------------------
    def run(self, df):

        print("\n" + "=" * 60)
        print("CUSTOMER SEGMENTATION")
        print("=" * 60)

        # Step 1 : Create RFM Features
        rfm = self.create_rfm(df)

        # Step 2 : Train KMeans
        segmented = self.train_model(rfm)

        # Step 3 : Save CSV
        self.save_segments(segmented)

        # Step 4 : Charts
        self.cluster_distribution(segmented)

        self.customer_segments(segmented)

        print("\n" + "=" * 60)
        print("CUSTOMER SEGMENTATION COMPLETED")
        print("=" * 60)

        print("\nFirst Five Customers\n")
        print(segmented.head())

        print("\nTotal Customers :", len(segmented))

        print("\nTotal Clusters :", segmented["Cluster"].nunique())

        return segmented