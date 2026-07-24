"""
============================================================
NeuralRetail - AI Retail Analytics Platform
Main Entry Point
============================================================
"""

# ==========================================================
# IMPORT MODULES
# ==========================================================

from src.preprocessing.data_loader import DataLoader
from src.preprocessing.data_analysis import DataAnalysis
from src.preprocessing.data_cleaning import DataCleaning
from src.feature_engineering.feature_engineering import FeatureEngineering
from src.eda.exploratory_data_analysis import ExploratoryDataAnalysis
from src.segmentation.customer_segmentation import CustomerSegmentation
from src.forecasting.sales_forecasting import SalesForecasting
from src.churn.customer_churn import CustomerChurn
from src.inventory.inventory_optimization import InventoryOptimization
from src.pricing.price_optimization import PriceOptimization
from src.recommendation.business_recommendation import BusinessRecommendation



# ==========================================================
# MAIN FUNCTION
# ==========================================================

def main():

    print("\n")
    print("=" * 80)
    print("          NEURALRETAIL - AI RETAIL ANALYTICS PLATFORM")
    print("=" * 80)

    # ======================================================
    # STEP 1 : DATA LOADING
    # ======================================================

    print("\n")
    print("=" * 80)
    print("STEP 1 : DATA LOADING")
    print("=" * 80)

    loader = DataLoader()
    df = loader.load_dataset()

    if df is None:
        print("Dataset could not be loaded.")
        return

    # ======================================================
    # STEP 2 : DATA ANALYSIS
    # ======================================================

    print("\n")
    print("=" * 80)
    print("STEP 2 : DATA ANALYSIS")
    print("=" * 80)

    analysis = DataAnalysis()

    analysis.dataset_shape(df)
    analysis.dataset_columns(df)
    analysis.data_types(df)
    analysis.missing_values(df)
    analysis.duplicate_rows(df)
    analysis.statistical_summary(df)
    analysis.customer_count(df)
    analysis.product_count(df)
    analysis.country_count(df)
    analysis.top_rows(df)

    # ======================================================
    # STEP 3 : DATA CLEANING
    # ======================================================

    print("\n")
    print("=" * 80)
    print("STEP 3 : DATA CLEANING")
    print("=" * 80)

    cleaner = DataCleaning()

    clean_df = cleaner.clean_dataset(df)

    cleaner.save_dataset(clean_df)

    print("\nData Cleaning Completed Successfully")
    print(clean_df.head())

    # ======================================================
    # STEP 4 : FEATURE ENGINEERING
    # ======================================================

    print("\n")
    print("=" * 80)
    print("STEP 4 : FEATURE ENGINEERING")
    print("=" * 80)

    feature = FeatureEngineering()

    feature_df = feature.create_features(clean_df)

    feature.save_dataset(feature_df)

    print("\nFeature Engineering Completed Successfully")
    print(feature_df.head())

        # ======================================================
    # STEP 5 : EXPLORATORY DATA ANALYSIS
    # ======================================================

    print("\n")
    print("=" * 80)
    print("STEP 5 : EXPLORATORY DATA ANALYSIS")
    print("=" * 80)

    eda = ExploratoryDataAnalysis()

    eda.monthly_sales(feature_df)
    eda.top_products(feature_df)
    eda.top_customers(feature_df)
    eda.country_sales(feature_df)
    eda.correlation_heatmap(feature_df)

    print("\nEDA Completed Successfully.")

    # ======================================================
    # STEP 6 : CUSTOMER SEGMENTATION
    # ======================================================

    print("\n")
    print("=" * 80)
    print("STEP 6 : CUSTOMER SEGMENTATION")
    print("=" * 80)

    segmentation = CustomerSegmentation()

    customer_segments = segmentation.run(feature_df)

    if customer_segments is not None:

        print("\nCustomer Segmentation Completed Successfully.")

        print("\nCustomer Segments Preview:\n")

        print(customer_segments.head())

    # ======================================================
    # STEP 7 : SALES FORECASTING
    # ======================================================

    print("\n")
    print("=" * 80)
    print("STEP 7 : SALES FORECASTING")
    print("=" * 80)

    forecasting = SalesForecasting()

    forecast_df = forecasting.run(feature_df)

    if forecast_df is not None:

        print("\nSales Forecasting Completed Successfully.")

        print("\nForecast Preview:\n")

        print(forecast_df.head())

    # ======================================================
    # STEP 8 : CUSTOMER CHURN PREDICTION
    # ======================================================

    print("\n")
    print("=" * 80)
    print("STEP 8 : CUSTOMER CHURN PREDICTION")
    print("=" * 80)

    churn = CustomerChurn()

    churn_df = churn.run(feature_df)

    if churn_df is not None:

        print("\nCustomer Churn Prediction Completed Successfully.")

        print("\nPrediction Preview:\n")

        print(churn_df.head())
    
        # ======================================================
    # STEP 9 : INVENTORY OPTIMIZATION
    # ======================================================

    print("\n")
    print("=" * 80)
    print("STEP 9 : INVENTORY OPTIMIZATION")
    print("=" * 80)

    inventory = InventoryOptimization()

    inventory_df = inventory.run(feature_df)

    if inventory_df is not None:

        print("\nInventory Optimization Completed Successfully.")

        print("\nInventory Preview:\n")

        print(inventory_df.head())

    # ======================================================
    # STEP 10 : PRICE OPTIMIZATION
    # ======================================================

    print("\n")
    print("=" * 80)
    print("STEP 10 : PRICE OPTIMIZATION")
    print("=" * 80)

    pricing = PriceOptimization()

    price_df = pricing.run(feature_df)

    if price_df is not None:

        print("\nPrice Optimization Completed Successfully.")

        print("\nPrice Preview:\n")

        print(price_df.head())

    # ======================================================
    # STEP 11 : BUSINESS RECOMMENDATION SYSTEM
    # ======================================================

    print("\n")
    print("=" * 80)
    print("STEP 11 : BUSINESS RECOMMENDATION SYSTEM")
    print("=" * 80)

    recommendation = BusinessRecommendation()

    recommendation_df = recommendation.run(feature_df)

    if recommendation_df is not None:

        print("\nBusiness Recommendation System Completed Successfully.")

        print("\nRecommendation Preview:\n")

        print(recommendation_df.head())

  

    # ======================================================
    # PROJECT SUMMARY
    # ======================================================

    print("\n")
    print("=" * 80)
    print("PROJECT SUMMARY")
    print("=" * 80)

    completed_modules = [
        "Dataset Loaded",
        "Data Analysis",
        "Data Cleaning",
        "Feature Engineering",
        "Exploratory Data Analysis",
        "Customer Segmentation",
        "Sales Forecasting",
        "Customer Churn Prediction",
        "Inventory Optimization",
        "Price Optimization",
        "Business Recommendation System",
        "Model Evaluation"
    ]

    for module in completed_modules:
        print(f"✓ {module}")

    print("\nGenerated CSV Files")
    print("-" * 40)

    csv_files = [
        "clean_data.csv",
        "featured_data.csv",
        "customer_segments.csv",
        "forecasted_sales.csv",
        "churn_prediction.csv",
        "inventory_status.csv",
        "price_optimization.csv",
        "business_recommendations.csv",
        "model_evaluation.csv"
    ]

    for file in csv_files:
        print(f"data/processed/{file}")

    print("\nGenerated Models")
    print("-" * 40)

    model_files = [
        "kmeans_model.pkl",
        "sales_forecasting_model.pkl",
        "churn_model.pkl",
        "inventory_model.pkl",
        "price_optimization_model.pkl",
        "recommendation_rules.pkl"
    ]

    for model in model_files:
        print(f"models/{model}")

    print("\nGenerated Images")
    print("-" * 40)

    image_files = [

        "monthly_sales.png",
        "top_products.png",
        "top_customers.png",
        "country_sales.png",
        "correlation_heatmap.png",

        "elbow_method.png",
        "cluster_distribution.png",
        "customer_segments.png",

        "historical_sales.png",
        "forecast_sales.png",
        "actual_vs_predicted.png",
        "monthly_sales_prediction.png",
        "feature_importance.png",

        "churn_distribution.png",
        "churn_feature_importance.png",
        "confusion_matrix.png",
        "roc_curve.png",

        "top_selling_products.png",
        "inventory_status.png",
        "low_stock_products.png",

        "price_distribution.png",
        "revenue_vs_price.png",
        "top_profitable_products.png",
        "discount_recommendation.png",

        "recommendation_distribution.png",
        "top_revenue_products.png",

        "model_comparison.png",
        "model_scores.png"
    ]

    for image in image_files:
        print(f"images/{image}")

    print("\n")
    print("=" * 80)
    print("NEURALRETAIL AI RETAIL ANALYTICS PLATFORM COMPLETED SUCCESSFULLY")
    print("=" * 80)


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":
    main()