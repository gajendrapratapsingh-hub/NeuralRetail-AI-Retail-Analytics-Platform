"""
===========================================================
NeuralRetail
Professional Sales Forecasting Module
===========================================================
"""

import os
import joblib
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

from sklearn.model_selection import train_test_split


class SalesForecasting:

    def __init__(self):

        os.makedirs("models", exist_ok=True)
        os.makedirs("images", exist_ok=True)
        os.makedirs("data/processed", exist_ok=True)

    # -----------------------------------------------------
    # Prepare Daily Sales
    # -----------------------------------------------------

    def prepare_data(self, df):

        print("\n" + "="*60)
        print("PREPARING SALES DATA")
        print("="*60)

        df = df.copy()

        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

        sales = (

            df.groupby(df["InvoiceDate"].dt.date)

            ["TotalPrice"]

            .sum()

            .reset_index()

        )

        sales.columns = [

            "Date",

            "Sales"

        ]

        sales["Date"] = pd.to_datetime(sales["Date"])

        print("Daily Sales Prepared Successfully")

        return sales

    # -----------------------------------------------------
    # Feature Engineering
    # -----------------------------------------------------

    def create_features(self, sales):

        print("\nCreating Time Features...")

        sales = sales.copy()

        sales["Day"] = np.arange(len(sales))

        sales["Month"] = sales["Date"].dt.month

        sales["Week"] = sales["Date"].dt.isocalendar().week.astype(int)

        sales["DayOfWeek"] = sales["Date"].dt.dayofweek

        sales["Quarter"] = sales["Date"].dt.quarter

        print("Features Created Successfully")

        return sales

    # -----------------------------------------------------
    # Train Test Split
    # -----------------------------------------------------

    def split_data(self, sales):

        X = sales[[

            "Day",

            "Month",

            "Week",

            "DayOfWeek",

            "Quarter"

        ]]

        y = sales["Sales"]

        X_train, X_test, y_train, y_test = train_test_split(

            X,

            y,

            test_size=0.20,

            shuffle=False,

            random_state=42

        )

        return X_train, X_test, y_train, y_test
        # -----------------------------------------------------
    # Train Random Forest Model
    # -----------------------------------------------------

    def train_model(self, X_train, y_train):

        print("\n" + "=" * 60)
        print("TRAINING RANDOM FOREST MODEL")
        print("=" * 60)

        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train, y_train)

        joblib.dump(
            model,
            "models/sales_forecasting_model.pkl"
        )

        print("Model Saved Successfully")

        return model

    # -----------------------------------------------------
    # Evaluate Model
    # -----------------------------------------------------

    def evaluate_model(self, model, X_test, y_test):

        print("\nEvaluating Model...")

        prediction = model.predict(X_test)

        mae = mean_absolute_error(y_test, prediction)

        rmse = np.sqrt(
            mean_squared_error(y_test, prediction)
        )

        r2 = r2_score(y_test, prediction)

        print("\nMODEL PERFORMANCE")
        print("-" * 40)
        print(f"MAE  : {mae:.2f}")
        print(f"RMSE : {rmse:.2f}")
        print(f"R²   : {r2:.4f}")

        return prediction

    # -----------------------------------------------------
    # Forecast Next 30 Days
    # -----------------------------------------------------

    def forecast_future(self, model, sales):

        print("\nForecasting Next 30 Days...")

        last_day = sales["Day"].max()

        future_dates = pd.date_range(
            start=sales["Date"].max() + pd.Timedelta(days=1),
            periods=30,
            freq="D"
        )

        future = pd.DataFrame({

            "Day": np.arange(
                last_day + 1,
                last_day + 31
            ),

            "Month": future_dates.month,

            "Week": future_dates.isocalendar().week.astype(int),

            "DayOfWeek": future_dates.dayofweek,

            "Quarter": future_dates.quarter

        })

        prediction = model.predict(future)

        forecast = pd.DataFrame({

            "Date": future_dates,

            "PredictedSales": prediction

        })

        forecast.to_csv(

            "data/processed/forecasted_sales.csv",

            index=False

        )

        print("Forecast Saved Successfully")

        return forecast

    # -----------------------------------------------------
    # Feature Importance
    # -----------------------------------------------------

    def feature_importance(self, model):

        print("\nGenerating Feature Importance...")

        names = [

            "Day",

            "Month",

            "Week",

            "DayOfWeek",

            "Quarter"

        ]

        importance = pd.Series(

            model.feature_importances_,

            index=names

        )

        plt.figure(figsize=(8,5))

        importance.sort_values().plot(kind="barh")

        plt.title("Feature Importance")

        plt.tight_layout()

        plt.savefig(

            "images/feature_importance.png",

            dpi=300

        )

        plt.close()

        print("Feature Importance Saved")
            # -----------------------------------------------------
    # Historical Sales Chart
    # -----------------------------------------------------

    def historical_sales_chart(self, sales):

        print("\nGenerating Historical Sales Chart...")

        plt.figure(figsize=(14,6))

        plt.plot(
            sales["Date"],
            sales["Sales"],
            linewidth=2
        )

        plt.title("Historical Sales")
        plt.xlabel("Date")
        plt.ylabel("Revenue")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            "images/historical_sales.png",
            dpi=300
        )

        plt.close()

        print("Historical Sales Chart Saved")

    # -----------------------------------------------------
    # Actual vs Predicted Chart
    # -----------------------------------------------------

    def actual_vs_predicted(self, y_test, prediction):

        print("\nGenerating Actual vs Predicted Chart...")

        plt.figure(figsize=(12,6))

        plt.plot(
            y_test.values,
            label="Actual",
            linewidth=2
        )

        plt.plot(
            prediction,
            label="Predicted",
            linewidth=2
        )

        plt.legend()

        plt.title("Actual vs Predicted Sales")

        plt.xlabel("Test Samples")

        plt.ylabel("Sales")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            "images/actual_vs_predicted.png",
            dpi=300
        )

        plt.close()

        print("Actual vs Predicted Chart Saved")

    # -----------------------------------------------------
    # Future Forecast Chart
    # -----------------------------------------------------

    def future_forecast_chart(self, sales, forecast):

        print("\nGenerating Forecast Chart...")

        plt.figure(figsize=(14,6))

        plt.plot(
            sales["Date"],
            sales["Sales"],
            label="Historical Sales",
            linewidth=2
        )

        plt.plot(
            forecast["Date"],
            forecast["PredictedSales"],
            label="Forecast",
            linewidth=2
        )

        plt.legend()

        plt.title("Next 30 Days Sales Forecast")

        plt.xlabel("Date")

        plt.ylabel("Revenue")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            "images/forecast_sales.png",
            dpi=300
        )

        plt.close()

        print("Forecast Chart Saved")

    # -----------------------------------------------------
    # Monthly Sales Chart
    # -----------------------------------------------------

    def monthly_sales_chart(self, df):

        print("\nGenerating Monthly Sales Chart...")

        monthly = (

            df.groupby("Month")["TotalPrice"]

            .sum()

        )

        plt.figure(figsize=(10,5))

        plt.bar(
            monthly.index.astype(str),
            monthly.values
        )

        plt.title("Monthly Sales")

        plt.xlabel("Month")

        plt.ylabel("Revenue")

        plt.tight_layout()

        plt.savefig(
            "images/monthly_sales_prediction.png",
            dpi=300
        )

        plt.close()

        print("Monthly Sales Chart Saved")

    # -----------------------------------------------------
    # Complete Pipeline
    # -----------------------------------------------------

    def run(self, df):

        try:

            sales = self.prepare_data(df)

            sales = self.create_features(sales)

            X_train, X_test, y_train, y_test = self.split_data(sales)

            model = self.train_model(
                X_train,
                y_train
            )

            prediction = self.evaluate_model(
                model,
                X_test,
                y_test
            )

            forecast = self.forecast_future(
                model,
                sales
            )

            self.feature_importance(model)

            self.historical_sales_chart(sales)

            self.actual_vs_predicted(
                y_test,
                prediction
            )

            self.future_forecast_chart(
                sales,
                forecast
            )

            self.monthly_sales_chart(df)

            print("\n")
            print("="*70)
            print("SALES FORECASTING COMPLETED SUCCESSFULLY")
            print("="*70)

            print("\nForecast Preview\n")

            print(forecast.head())

            return forecast

        except Exception as e:

            print("\nSales Forecasting Failed!")

            print(e)

            return None