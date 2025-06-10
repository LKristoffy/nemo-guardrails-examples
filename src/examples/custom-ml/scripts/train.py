try:
    from .generate_data import create_synthetic_dataset
except ImportError:
    from generate_data import create_synthetic_dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os

def train_model():
    """
    Train a model on the synthetic dataset and save it to a CSV file.
    """
    # Create synthetic dataset
    df = create_synthetic_dataset(n_samples=1000, bias_level=0.3)
    
    # Split into train and test
    train_df, test_df = train_test_split(df, test_size=0.3, random_state=42)

    # Train a logistic regression model
    print("Training logistic regression model...")
    X_train = train_df[["X1", "X2"]]
    print(X_train.head())

    y_train = train_df["target"]
    model = LogisticRegression(C=0.1, solver='liblinear')
    model.fit(X_train, y_train)

    # Prepare test data
    X_test = test_df[["X1", "X2"]]
    test_df["y_pred"] = model.predict(X_test)

    # Save the test DataFrame to a CSV file
    # Get the absolute path to ensure correct directory creation
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    csv_path = os.path.join(data_dir, "test_data.csv")
    test_df.to_csv(csv_path, index=False)
    print(f"Model trained and test data saved to '{csv_path}'.")

if __name__ == "__main__":
    train_model()
