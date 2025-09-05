import pandas as pd
import numpy as np
import xgboost as xgb
from scipy import interpolate
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import optuna
import joblib
import os

def load_data(train_path, test_path):
    """Load training and test datasets"""
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    return train, test

def preprocess_data(df, is_train=True, scaler=None):
    """Preprocess the dataset"""
    # Drop unnecessary columns
    columns_to_drop = ['Employee ID', 'Date of Joining']
    existing_cols = [col for col in columns_to_drop if col in df.columns]
    if existing_cols:
        df = df.drop(columns=existing_cols)
    
    # One-hot encoding
    is_male = pd.get_dummies(df.Gender, drop_first=True)
    is_service = pd.get_dummies(df['Company Type'], drop_first=True)
    wfh_available = pd.get_dummies(df['WFH Setup Available'], drop_first=True)
    
    # Insert encoded columns
    for loc, column in enumerate(["is_male", "is_service", "wfh_available"], start=2):
        df.insert(loc=loc, column=column, value=eval(column))
    
    df.drop(columns=["Gender", "Company Type", "WFH Setup Available"], axis=1, inplace=True)
    
    if is_train:
        # Handle missing target values for training data
        missing_target_rows = df.loc[df['Burn Rate'].isna(), :].index
        df = df.drop(missing_target_rows, axis=0).reset_index(drop=True)
        
        # Handle missing values using interpolation
        df = handle_missing_values(df)
        
        # Remove outliers
        df = remove_outliers(df, ['Resource Allocation', 'Mental Fatigue Score'])

        df, scaler = scale_features(df, is_train=True)
        return df, scaler
    else:
        df, _ = scale_features(df, scaler=scaler, is_train=False)
        return df, scaler

def handle_missing_values(df):
    """Handle missing values in the dataset"""
    # Create interpolation function for Mental Fatigue Score
    train_copy = df.copy(deep=True)
    mental_not_na = train_copy['Mental Fatigue Score'].notna()
    burn_not_na = train_copy['Burn Rate'].notna()
    train_copy = train_copy[(mental_not_na) & (burn_not_na)]
    
    if len(train_copy) > 1:
        fn_mental = interpolate.interp1d(
            y=train_copy['Mental Fatigue Score'],
            x=train_copy['Burn Rate'],
            kind="linear",
            fill_value="extrapolate"
        )
        
        # Fill missing Mental Fatigue Scores
        for i in df[df['Mental Fatigue Score'].isna()].index:
            df.loc[i, 'Mental Fatigue Score'] = fn_mental(df.loc[i, 'Burn Rate'])
    
    # Group-wise imputation for Resource Allocation
    for i in range(6):
        mean_value = df['Resource Allocation'][df['Designation']==i].mean()
        condition = (df['Designation']==i) & (df['Resource Allocation'].isna())
        df.loc[condition, 'Resource Allocation'] = mean_value
    
    return df

def remove_outliers(df, columns):
    """Remove outliers using IQR method by capping them"""
    df_clean = df.copy()
    
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
    
    return df_clean

def scale_features(df, scaler=None, is_train=True):
    """
    Scale numeric features
    Features with different scales can bias certain machine learning algorithms.
    Standardization ensures all features contribute equally to the model.
    """

    numeric_cols = ['Resource Allocation', 'Mental Fatigue Score']
    # Scale the features
    df_scaled = df.copy()

    if is_train:
        scaler = StandardScaler()
        df_scaled[numeric_cols] = scaler.fit_transform(df[numeric_cols])

        # Save scaler for later use
        os.makedirs("models", exist_ok=True)
        joblib.dump(scaler, "models/feature_scaler.pkl")

        return df_scaled, scaler
    else:
        # Load and apply scaler for test/validation data
        if scaler is None:
            scaler = joblib.load("models/feature_scaler.pkl")

        df_scaled[numeric_cols] = scaler.transform(df[numeric_cols])
        return df_scaled, scaler

def optimize_model(X_train, y_train, n_trials=200):
    """Optimize XGBoost hyperparameters using Optuna"""
    def objective(trial):
        params = {
            'objective': 'reg:squarederror',
            'eval_metric': 'rmse',
            'booster': 'gbtree',
            'max_depth': trial.suggest_int('max_depth', 3, 15),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            'n_estimators': trial.suggest_int('n_estimators', 100, 2000),
            'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            'early_stopping_rounds': 50,
            'random_state': 42
        }

        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        scores = []

        for train_idx, valid_idx in kf.split(X_train):
            X_t, X_v = X_train.iloc[train_idx], X_train.iloc[valid_idx]
            y_t, y_v = y_train.iloc[train_idx], y_train.iloc[valid_idx]

            model = xgb.XGBRegressor(**params)
            model.fit(X_t, y_t, eval_set=[(X_v, y_v)], verbose=False)

            y_pred = model.predict(X_v)
            scores.append(r2_score(y_v, y_pred))

        return np.mean(scores)
    
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
    
    return study.best_params

def train_model(X_train, y_train, best_params):
    """Train the final model with best parameters"""
    final_model = xgb.XGBRegressor(
        objective='reg:squarederror',
        eval_metric='rmse',
        booster='gbtree',
        **best_params
    )
    final_model.fit(X_train, y_train)

    lower_model = xgb.XGBRegressor(
        objective='reg:quantileerror', 
        quantile_alpha=0.01, 
        **best_params
    )
    lower_model.fit(X_train, y_train)

    upper_model = xgb.XGBRegressor(
        objective='reg:quantileerror',
        quantile_alpha=0.99,
        **best_params
    )
    upper_model.fit(X_train, y_train)

    return final_model, lower_model, upper_model

def evaluate_model(model, X_train, y_train, X_val, y_val):
    """Evaluate model performance"""
    train_preds = model.predict(X_train)
    val_preds = model.predict(X_val)
    
    print("=== MODEL PERFORMANCE ===")
    print(f"Training R²:   {r2_score(y_train, train_preds):.4f}")
    print(f"Validation R²: {r2_score(y_val, val_preds):.4f}")
    print(f"Training RMSE: {np.sqrt(mean_squared_error(y_train, train_preds)):.4f}")
    print(f"Validation RMSE: {np.sqrt(mean_squared_error(y_val, val_preds)):.4f}")
    print(f"Training MAE:  {mean_absolute_error(y_train, train_preds):.4f}")
    print(f"Validation MAE: {mean_absolute_error(y_val, val_preds):.4f}")
    
    r2_diff = r2_score(y_train, train_preds) - r2_score(y_val, val_preds)
    print(f"\nOverfitting check (R² difference): {r2_diff:.4f}")
    if r2_diff > 0.1:
        print("Model may be overfitting!")
    else:
        print("Model generalization looks good.")

def categorize_burnout_risk(burn_rate):
    """Categorize burnout risk based on burn rate"""
    if burn_rate <= 0.3:
        return 'Low Risk'
    elif burn_rate <= 0.6:
        return 'Medium Risk'
    else:
        return 'High Risk'

def predict_single_employee(model, designation, resource_allocation, mental_fatigue, 
                           is_male, is_service, wfh_available):
    """Predict burnout risk for a single employee"""
    employee_data = pd.DataFrame({
        'is_male': [is_male],
        'is_service': [is_service],
        'wfh_available': [wfh_available],
        'Designation': [designation],
        'Resource Allocation': [resource_allocation],
        'Mental Fatigue Score': [mental_fatigue]
    })

    print("Before scaling:")
    print(employee_data)

    try:
        scaler = joblib.load("models/feature_scaler.pkl")
        numeric_cols = ['Resource Allocation', 'Mental Fatigue Score']
        employee_data[numeric_cols] = scaler.transform(employee_data[numeric_cols])

        print("After scaling:")
        print(employee_data)
    except FileNotFoundError:
        print("Warning: Scaler not found. Predictions may be inaccurate.")
        return None, None, None

    # Load quantile models for confidence calculation
    try:
        lower_model = joblib.load("models/lower_quantile_model.pkl")
        upper_model = joblib.load("models/upper_quantile_model.pkl")
    except FileNotFoundError:
        print("Warning: Quantile models not found. Confidence score unavailable.")
        lower_model, upper_model = None, None
    
    prediction = model.predict(employee_data)[0]
    prediction = np.clip(prediction, 0, 1) # Clip final prediction to valid range
    risk = categorize_burnout_risk(prediction)

    # Calculate confidence score
    confidence = 0.5 # Default confidence
    if lower_model and upper_model:
        lower_bound = lower_model.predict(employee_data)[0]
        upper_bound = upper_model.predict(employee_data)[0]
        interval_width = abs(upper_bound - lower_bound)
        # Confidence is inversely proportional to the interval width
        confidence = max(0.0, 1.0 - interval_width)

    print(f"Raw prediction: {prediction}")
    
    return prediction, risk, confidence

def main():
    """Main execution function"""
    # Load data
    print("Loading data...")
    train, test = load_data("input/train.csv", "input/test.csv")
    
    # Preprocess data
    print("Preprocessing training data...")
    train_processed, scaler = preprocess_data(train, is_train=True)

    X = train_processed.drop('Burn Rate', axis=1)
    y = train_processed['Burn Rate']

    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, shuffle=True, random_state=42
    )
        
    print(f"Training set shape: {X_train.shape}")
    print(f"Validation set shape: {X_val.shape}")

    test_processed, _ = preprocess_data(test, is_train=False, scaler=scaler)
    


    
    # Optimize hyperparameters
    print("Optimizing hyperparameters...")
    best_params = optimize_model(X_train, y_train, n_trials=100)  
    print("Best hyperparameters:", best_params)
    
    # Train final model
    print("Training final model...")
    model, lower_model, upper_model = train_model(X_train, y_train, best_params)
    
    # Evaluate model
    evaluate_model(model, X_train, y_train, X_val, y_val)

    # Save models
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/burnout_prediction_model.pkl")
    joblib.dump(lower_model, "models/lower_quantile_model.pkl")
    joblib.dump(upper_model, "models/upper_quantile_model.pkl")
    print("All models saved to models directory")
    
    # Make predictions on test set
    print("Making predictions on test set...")
    test_predictions = model.predict(test_processed)
    
    # Create results DataFrame
    results = pd.DataFrame({
        'Employee_Index': range(len(test_predictions)),
        'Predicted_Burn_Rate': test_predictions,
        'Risk_Category': [categorize_burnout_risk(rate) for rate in test_predictions]
    })
    
    # Save results
    os.makedirs("outputs", exist_ok=True)
    results.to_csv('outputs/burnout_predictions.csv', index=False)
    print("Predictions saved to outputs/burnout_predictions.csv")
    
    # Example prediction
    print("\n=== EXAMPLE PREDICTION ===")
    burn_rate, risk, confidence = predict_single_employee(
        model, designation=3, resource_allocation=10, mental_fatigue=4.5,
        is_male=1, is_service=0, wfh_available=1
    )
    if burn_rate is not None: 
        print(f"Risk Category: {risk}")
        print(f"Predicted Burn Rate: {burn_rate:.4f}")
        print(f"Confidence Score: {confidence:.4f}")


if __name__ == "__main__":
    main()