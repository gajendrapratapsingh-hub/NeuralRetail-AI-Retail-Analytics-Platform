import pandas as pd
import os


class DataLoader:

    def __init__(self):

        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

        self.dataset_path = os.path.join(
            project_root,
            "data",
            "raw",
            "OnlineRetail.csv"
        )

        print("Dataset Path:", self.dataset_path)

    def load_dataset(self):

        print("=" * 60)
        print("Loading Dataset...")
        print("=" * 60)

        if not os.path.exists(self.dataset_path):
            print("❌ Dataset not found!")
            return None

        df = pd.read_csv(
            self.dataset_path,
            encoding="ISO-8859-1"
        )

        print("✅ Dataset Loaded Successfully!")

        return df