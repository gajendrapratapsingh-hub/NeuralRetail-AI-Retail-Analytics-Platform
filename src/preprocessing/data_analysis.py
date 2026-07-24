"""
NeuralRetail
Dataset Analysis Module
"""

class DataAnalysis:

    def dataset_shape(self, df):

        print("\n" + "="*60)
        print("DATASET SHAPE")
        print("="*60)

        print(f"Rows    : {df.shape[0]}")
        print(f"Columns : {df.shape[1]}")


    def dataset_columns(self, df):

        print("\n" + "="*60)
        print("COLUMN NAMES")
        print("="*60)

        for column in df.columns:
            print(column)


    def data_types(self, df):

        print("\n" + "="*60)
        print("DATA TYPES")
        print("="*60)

        print(df.dtypes)


    def missing_values(self, df):

        print("\n" + "="*60)
        print("MISSING VALUES")
        print("="*60)

        print(df.isnull().sum())


    def duplicate_rows(self, df):

        print("\n" + "="*60)
        print("DUPLICATE ROWS")
        print("="*60)

        print(df.duplicated().sum())


    def statistical_summary(self, df):

        print("\n" + "="*60)
        print("STATISTICAL SUMMARY")
        print("="*60)

        print(df.describe())


    def customer_count(self, df):

        print("\n" + "="*60)
        print("TOTAL CUSTOMERS")
        print("="*60)

        print(df["CustomerID"].nunique())


    def product_count(self, df):

        print("\n" + "="*60)
        print("TOTAL PRODUCTS")
        print("="*60)

        print(df["StockCode"].nunique())


    def country_count(self, df):

        print("\n" + "="*60)
        print("TOTAL COUNTRIES")
        print("="*60)

        print(df["Country"].nunique())


    def top_rows(self, df):

        print("\n" + "="*60)
        print("FIRST FIVE RECORDS")
        print("="*60)

        print(df.head())