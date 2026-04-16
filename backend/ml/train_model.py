# train_model.py — Train the Random Forest model and save it

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

def train_and_save_model():
    """Load CSV, train Random Forest, save model to disk."""

    # Get path to CSV relative to this file's location
    csv_path = os.path.join(os.path.dirname(__file__), "login_data.csv")

    # Check if CSV file exists
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found")
        return None

    # Load CSV into a Pandas DataFrame
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows from login_data.csv")

    # X = features (all columns except 'label')
    # y = target labels (the 'label' column)
    X = df.drop("label", axis=1)   # axis=1 means drop a column (not a row)
    y = df["label"]

    # Split data: 80% training, 20% testing
    # random_state=42 makes the split reproducible
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Create Random Forest with 100 decision trees
    # n_estimators=100 means 100 trees vote on each prediction
    # random_state=42 for reproducibility
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model on training data
    model.fit(X_train, y_train)

    # Evaluate on test data
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save the trained model to a .pkl file using pickle
    model_path = os.path.join(os.path.dirname(__file__), "rf_model.pkl")
    with open(model_path, "wb") as f:   # "wb" = write binary
        pickle.dump(model, f)

    print(f"Model saved to {model_path}")
    return model

if __name__ == "__main__":
    train_and_save_model()