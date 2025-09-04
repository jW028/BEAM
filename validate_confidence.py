import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

# --- Configuration ---
MODEL_PATH = "models/burnout_prediction_model.pkl"
LOWER_MODEL_PATH = "models/lower_quantile_model.pkl"
UPPER_MODEL_PATH = "models/upper_quantile_model.pkl"
SCALER_PATH = "models/feature_scaler.pkl"
DATA_PATH = "input/train.csv"

def validate_confidence_logic():
    """
    Validates both the quantile regression models and the API confidence calculation
    """
    print("--- Starting Confidence Score Validation ---")

    # 1. Load all necessary files
    try:
        model = joblib.load(MODEL_PATH)
        lower_model = joblib.load(LOWER_MODEL_PATH)
        upper_model = joblib.load(UPPER_MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        df = pd.read_csv(DATA_PATH)
        print("✅ Models, scaler, and data loaded successfully.")
    except FileNotFoundError as e:
        print(f"❌ Error loading files: {e}. Make sure all models are trained and paths are correct.")
        return

    # 2. Recreate preprocessing (simplified for validation)
    df.dropna(subset=['Burn Rate'], inplace=True)
    df.fillna(df.median(numeric_only=True), inplace=True)
    is_male = pd.get_dummies(df.Gender, drop_first=True)
    is_service = pd.get_dummies(df['Company Type'], drop_first=True)
    wfh_available = pd.get_dummies(df['WFH Setup Available'], drop_first=True)
    df.insert(loc=2, column="is_male", value=is_male)
    df.insert(loc=3, column="is_service", value=is_service)
    df.insert(loc=4, column="wfh_available", value=wfh_available)
    df.drop(columns=["Gender", "Company Type", "WFH Setup Available", "Employee ID", "Date of Joining"], inplace=True)
    
    X = df.drop('Burn Rate', axis=1)
    y = df['Burn Rate']
    
    # Apply scaling
    numeric_cols = ['Resource Allocation', 'Mental Fatigue Score']
    X[numeric_cols] = scaler.transform(X[numeric_cols])
    
    # Use the same random_state to get the identical validation set
    _, X_val, _, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Validation set created with {len(X_val)} samples.")

    # 3. Generate all predictions on the validation set
    median_preds = model.predict(X_val)
    lower_preds = lower_model.predict(X_val)
    upper_preds = upper_model.predict(X_val)

    # 4. Calculate Raw Interval Metrics
    is_covered = (y_val >= lower_preds) & (y_val <= upper_preds)
    coverage = np.mean(is_covered)
    interval_width = np.mean(abs(upper_preds - lower_preds))

    # 5. Calculate Model Confidence Scores
    interval_widths = abs(upper_preds - lower_preds)
    confidence_scores = np.maximum(0.0, np.minimum(1.0, 1.0 - interval_widths))

    mean_confidence = np.mean(confidence_scores)
    min_confidence = np.min(confidence_scores)
    max_confidence = np.max(confidence_scores)


    # 6. Print comprehensive validation results
    print("\n--- Raw Model Performance ---")
    print(f"🎯 Prediction Interval Coverage (PICP): {coverage:.2%}")
    print(f"   (Target for 91% interval: ~91.0%)")
    print(f"📏 Mean Interval Width: {interval_width:.4f}")

    print("\n--- Model Confidence Score Analysis ---")
    print(f"Mean Model Confidence: {mean_confidence:.1%}")
    print(f"Confidence Range: {min_confidence:.1%} - {max_confidence:.1%}")
    print("-" * 50)

    # 7. Interpret the results
    print("\n--- Interpretation ---")
    if 0.88 <= coverage <= 0.94:
        print("Model Performance: Coverage is reasonable.")
        print("Quantile models are statistically sound.")
    elif coverage >= 0.94:
        print("Model Performance: Excellent coverage.")
    else:
        print("Model Performance: Coverage too low.")


    # 8. Create enhanced visualization
    print("\nGenerating visualization...")
    sample_indices = np.random.choice(X_val.index, size=100, replace=False)
    
    median_preds_s = pd.Series(median_preds, index=X_val.index)
    lower_preds_s = pd.Series(lower_preds, index=X_val.index)
    upper_preds_s = pd.Series(upper_preds, index=X_val.index)
    api_confidence_s = pd.Series(confidence_scores, index=X_val.index)
    
    sorted_indices = median_preds_s.loc[sample_indices].sort_values().index

    # Create subplot with confidence scores
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
    
    # Plot 1: Prediction intervals
    ax1.plot(range(100), y_val.loc[sorted_indices], 'o', color='blue', label='True Burn Rate', markersize=5)
    ax1.plot(range(100), median_preds_s.loc[sorted_indices], '-', color='red', label='Predicted Burn Rate', linewidth=2)
    ax1.fill_between(
        range(100),
        lower_preds_s.loc[sorted_indices],
        upper_preds_s.loc[sorted_indices],
        color='red',
        alpha=0.2,
        label='91% Prediction Interval'
    )
    ax1.set_title('Prediction Interval Validation (100 Random Samples)', fontsize=14)
    ax1.set_xlabel('Sample Employee (Sorted by Prediction)', fontsize=12)
    ax1.set_ylabel('Burn Rate', fontsize=12)
    ax1.legend()
    ax1.grid(True)
    
    # Plot 2: API Confidence scores
    ax2.plot(range(100), api_confidence_s.loc[sorted_indices], 'o-', color='green', label='API Confidence Score', markersize=4)
    ax2.axhline(y=0.85, color='orange', linestyle='--', label='High Confidence Threshold')
    ax2.axhline(y=0.70, color='red', linestyle='--', label='Moderate Confidence Threshold')
    ax2.set_title('Model Confidence Scores for Same Samples', fontsize=14)
    ax2.set_xlabel('Sample Employee (Same Order as Above)', fontsize=12)
    ax2.set_ylabel('Model Confidence Score', fontsize=12)
    ax2.set_ylim(0, 1)
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

    # 9. Summary recommendations
    print("\n--- Recommendations ---")
    if mean_confidence < 0.70:
        print("🔧 Consider reducing calibration_factor further to increase confidence scores")
    if coverage < 0.89:
        print("🔧 Consider retraining quantile models with wider intervals (e.g., 2nd-98th percentile)")
    if coverage > 0.95:
        print("🔧 Consider retraining quantile models with tighter intervals (e.g., 10th-90th percentile)")

if __name__ == "__main__":
    validate_confidence_logic()