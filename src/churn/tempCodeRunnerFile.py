"""
===========================================================
NeuralRetail
Customer Churn Prediction
===========================================================
"""

import os
import joblib
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    RocCurveDisplay
)


class CustomerChurn:

    def __init__(self):

        os.makedirs("models", exist_ok=True)
        os.makedirs("images", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)

    # -------------------------------------------------------
    # Create Customer Features
    # -------------------------------------------------------

    def create_customer_features(self, df):

        print("\n" + "="*60)
        print("CREATING CUSTOMER FEATURES")
        print("="*60)

        df = df.copy()

        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

        latest_date = df["InvoiceDate"].max()

        customer = df.groupby("CustomerID").agg({

            "InvoiceDate": lambda x: (latest_date - x.max()).days,

            "InvoiceNo": "nunique",

            "Quantity": "sum",

            "TotalPrice": "sum"

        }).reset_index()

        customer.columns = [

            "CustomerID",
            "Recency",
            "Frequency",
            "Quantity",
            "Monetary"

        ]

        customer["AverageOrderValue"] = (

            customer["Monetary"] /

            customer["Frequency"]

        )

        print("Customer Features Created Successfully")

        return customer

    # -------------------------------------------------------
    # Create Churn Labels
    # -------------------------------------------------------

    def create_churn_label(self, customer):

        print("\nCreating Churn Labels...")

        customer["Churn"] = np.where(

            customer["Recency"] > 90,

            1,

            0

        )

        print(customer["Churn"].value_counts())

        return customer

    # -------------------------------------------------------
    # Prepare Dataset
    # -------------------------------------------------------

    def prepare_dataset(self, customer):

        X = customer[[

            "Recency",

            "Frequency",

            "Quantity",

            "Monetary",

            "AverageOrderValue"

        ]]

        y = customer["Churn"]

        scaler = StandardScaler()

        X = scaler.fit_transform(X)

        return train_test_split(

            X,

            y,

            test_size=0.20,

            random_state=42

        )
        # -------------------------------------------------------
    # Train Random Forest Model
    # -------------------------------------------------------

    def train_model(self, X_train, y_train):

        print("\n" + "="*60)
        print("TRAINING CUSTOMER CHURN MODEL")
        print("="*60)

        model = RandomForestClassifier(

            n_estimators=200,
            max_depth=10,
            random_state=42,
            n_jobs=-1

        )

        model.fit(X_train, y_train)

        joblib.dump(

            model,

            "models/churn_model.pkl"

        )

        print("Model Saved Successfully")

        return model

    # -------------------------------------------------------
    # Evaluate Model
    # -------------------------------------------------------

    def evaluate_model(

        self,

        model,

        X_test,

        y_test

    ):

        print("\nEvaluating Customer Churn Model...")

        prediction = model.predict(X_test)

        accuracy = accuracy_score(

            y_test,

            prediction

        )

        precision = precision_score(

            y_test,

            prediction,

            zero_division=0

        )

        recall = recall_score(

            y_test,

            prediction,

            zero_division=0

        )

        f1 = f1_score(

            y_test,

            prediction,

            zero_division=0

        )

        print("\nMODEL PERFORMANCE")

        print("-"*40)

        print(f"Accuracy  : {accuracy:.4f}")

        print(f"Precision : {precision:.4f}")

        print(f"Recall    : {recall:.4f}")

        print(f"F1 Score  : {f1:.4f}")

        return prediction

    # -------------------------------------------------------
    # Save Prediction CSV
    # -------------------------------------------------------

    def save_predictions(

        self,

        customer,

        model,

        scaler=None

    ):

        print("\nSaving Prediction File...")

        X = customer[[

            "Recency",

            "Frequency",

            "Quantity",

            "Monetary",

            "AverageOrderValue"

        ]]

        if scaler is not None:

            X = scaler.transform(X)

        else:

            scaler = StandardScaler()

            X = scaler.fit_transform(X)

        customer["PredictedChurn"] = model.predict(X)

        customer.to_csv(

            "data/processed/churn_prediction.csv",

            index=False

        )

        print("Prediction CSV Saved Successfully")

        return customer

    # -------------------------------------------------------
    # Feature Importance
    # -------------------------------------------------------

    def feature_importance(

        self,

        model

    ):

        print("\nGenerating Feature Importance...")

        features = [

            "Recency",

            "Frequency",

            "Quantity",

            "Monetary",

            "AverageOrderValue"

        ]

        importance = pd.Series(

            model.feature_importances_,

            index=features

        )

        plt.figure(figsize=(8,5))

        importance.sort_values().plot(

            kind="barh"

        )

        plt.title("Customer Churn Feature Importance")

        plt.tight_layout()

        plt.savefig(

            "images/churn_feature_importance.png",

            dpi=300

        )

        plt.close()

        print("Feature Importance Saved")
            # -------------------------------------------------------
    # Churn Distribution Chart
    # -------------------------------------------------------

    def churn_distribution(self, customer):

        print("\nGenerating Churn Distribution...")

        plt.figure(figsize=(7,5))

        customer["PredictedChurn"].value_counts().sort_index().plot(
            kind="bar"
        )

        plt.title("Customer Churn Distribution")
        plt.xlabel("Churn (0 = No, 1 = Yes)")
        plt.ylabel("Number of Customers")

        plt.tight_layout()

        plt.savefig(
            "images/churn_distribution.png",
            dpi=300
        )

        plt.close()

        print("Churn Distribution Saved")

    # -------------------------------------------------------
    # Confusion Matrix
    # -------------------------------------------------------

    def confusion_matrix_plot(

        self,

        y_test,

        prediction

    ):

        print("\nGenerating Confusion Matrix...")

        cm = confusion_matrix(

            y_test,

            prediction

        )

        disp = ConfusionMatrixDisplay(

            confusion_matrix=cm

        )

        disp.plot()

        plt.title("Confusion Matrix")

        plt.tight_layout()

        plt.savefig(

            "images/confusion_matrix.png",

            dpi=300

        )

        plt.close()

        print("Confusion Matrix Saved")

    # -------------------------------------------------------
    # ROC Curve
    # -------------------------------------------------------

    def roc_curve_plot(

        self,

        model,

        X_test,

        y_test

    ):

        print("\nGenerating ROC Curve...")

        RocCurveDisplay.from_estimator(

            model,

            X_test,

            y_test

        )

        plt.tight_layout()

        plt.savefig(

            "images/roc_curve.png",

            dpi=300

        )

        plt.close()

        print("ROC Curve Saved")

    # -------------------------------------------------------
    # Complete Pipeline
    # -------------------------------------------------------

    def run(self, df):

        try:

            customer = self.create_customer_features(df)

            customer = self.create_churn_label(customer)

            X_train, X_test, y_train, y_test = self.prepare_dataset(customer)

            model = self.train_model(

                X_train,

                y_train

            )

            prediction = self.evaluate_model(

                model,

                X_test,

                y_test

            )

            customer = self.save_predictions(

                customer,

                model

            )

            self.feature_importance(model)

            self.churn_distribution(customer)

            self.confusion_matrix_plot(

                y_test,

                prediction

            )

            self.roc_curve_plot(

                model,

                X_test,

                y_test

            )

            print("\n")
            print("="*70)
            print("CUSTOMER CHURN PREDICTION COMPLETED")
            print("="*70)

            print("\nPrediction Preview\n")

            print(customer.head())

            return customer

        except Exception as e:

            print("\nCustomer Churn Prediction Failed!")

            print(e)

            return None